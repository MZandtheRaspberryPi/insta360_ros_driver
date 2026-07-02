import os
import math

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import torchvision


IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/spot-day-out-rgb"
SELECTED_IMAGES = ["img_raw_0000002_0.056005239486694336.png"]
DEVICE = "cuda"
FOV = 180.0
IMG_SHAPE = (1920, 1920)

TRANSLATION = (0.0, 0.0, -0.105)
ROTATION = (-0.5, 0.0, 1.1)


def get_intrinsics(fov: float, width: float, height: float, device: str):
    f_x = width / (2 * math.tan(fov/2))
    f_y = f_x
    c_x = width / 2.0
    c_y = height / 2.0
    K = torch.tensor([[f_x, 0, c_x], [0, f_y, c_y], [0, 0, 1]], device=device, dtype=torch.float32)
    return K

@torch.inference_mode()
def main():
    
    all_imgs = os.listdir(IMG_DIR)
    all_imgs.sort()

    for img_name in all_imgs:

        if img_name not in SELECTED_IMAGES:
            continue

        full_path = os.path.join(IMG_DIR, img_name)
        print(full_path)

        img_arr = cv2.imread(full_path)
        img_arr_half = img_arr.shape[1] // 2

        img1 = img_arr[:, 0:img_arr_half, :]
        img2 = img_arr[:, img_arr_half:, :]

        img1_t = torch.tensor(img1, device=DEVICE)
        img2_t = torch.tensor(img2, device=DEVICE)
        print(img1_t.shape)

        K = get_intrinsics(math.pi * FOV/180.0, IMG_SHAPE[1], IMG_SHAPE[0], DEVICE)

        roll, pitch, yaw = ROTATION
        print(pitch)
        rx = torch.tensor([[1.0, 0.0, 0.0],
                            [0.0, math.cos(roll), -math.sin(roll)],
                            [0.0, math.sin(roll), math.cos(roll)]],
                            device=DEVICE, dtype=torch.float32)

        ry = torch.tensor([[math.cos(pitch), 0.0, math.sin(pitch)],
                            [0.0, 1.0, 0.0],
                            [-math.sin(pitch), 0.0, math.cos(pitch)]],
                            device=DEVICE, dtype=torch.float32)
        
        rz = torch.tensor([[math.cos(yaw), -math.sin(yaw), 0.0],
                            [math.sin(yaw), math.cos(yaw), 0.0],
                            [0.0, 0.0, 1.0]],
                            device=DEVICE, dtype=torch.float32)

        back_to_front_rotation = rz * ry * rx
        back_to_front_translation = torch.tensor(TRANSLATION, device=DEVICE, dtype=torch.float32)

        equirect_width = IMG_SHAPE[1]*2
        equirect_height = IMG_SHAPE[0]
        equirect_coords_x = torch.arange(0, equirect_width, device=DEVICE, dtype=torch.int32)
        equirect_coords_y = torch.arange(0, equirect_height, device=DEVICE, dtype=torch.int32)

        grid_x, grid_y = torch.meshgrid(equirect_coords_x, equirect_coords_y,  indexing='xy')

        print(f"Grid_x shape: {grid_x.shape}")
        print(grid_x[:, 0])
        print(grid_x[0, :])

        grid_y = grid_y.to(dtype=torch.float32)
        grid_x = grid_x.to(dtype=torch.float32)

        # convert equirectangular coordinates to spherical coordinates
        # x 0 in equirect coords corresponds to -pi azimuth, or lon

        azimuth = (torch.round(grid_x / float(equirect_width), decimals=5)) * 2 * math.pi - math.pi
        elevation = (torch.round(grid_y / float(equirect_height), decimals=5)) * math.pi - math.pi/2

        # azimuth = 2 * math.pi * (grid_x - 0.5)
        # elevation = math.pi * (grid_y - 0.5)

        # now to world coordinates

        x = 1.0 * torch.cos(elevation) * torch.sin(azimuth)
        y = 1.0 * torch.sin(elevation)
        z = 1.0 * torch.cos(elevation) * torch.cos(azimuth)

        front_mask = z >= 0.0
        front_x = x[front_mask]
        front_y = y[front_mask]
        front_z = z[front_mask]

        print(f"front_x shape: {front_x.shape}")


        r = torch.sqrt(front_x**2 + front_y**2)
        r[r<1e-6] = 1e-6

        theta = torch.atan2(r, torch.abs(front_z))
        r_fisheye = 2 * theta / math.pi * (float(IMG_SHAPE[1])/2.0)

        front_map_x = K[0, 2] + front_x/r * r_fisheye
        front_map_y = K[1, 2] + front_y / r * r_fisheye

        front_map_x = front_map_x.reshape(IMG_SHAPE[0], IMG_SHAPE[1])
        front_map_y = front_map_y.reshape(IMG_SHAPE[0], IMG_SHAPE[1])

        # --- Replicate cv2.BORDER_WRAP ---
        # cv2 wraps x around width and y around height
        x_grid = torch.remainder(front_map_x, IMG_SHAPE[1])
        y_grid = torch.remainder(front_map_y, IMG_SHAPE[0])

        # --- Normalize pixel coords to [-1, 1] for grid_sample ---
        x_norm = 2.0 * x_grid / (IMG_SHAPE[1] - 1) - 1.0
        y_norm = 2.0 * y_grid / (IMG_SHAPE[0] - 1) - 1.0

        grid = torch.stack([x_norm, y_norm], dim=-1).unsqueeze(0)  # (1, H_out, W_out, 2)

        # h x w x c to b x c x h x w
        img1_t = img1_t.permute(2, 0, 1).unsqueeze(0)

        # print(img1_t.dtype)
        front = F.grid_sample(
            img1_t.float(), grid,
            mode='bicubic',            # 'bicubic' ~ cv2.INTER_CUBIC
            padding_mode='zeros', # irrelevant now, coords are pre-wrapped
            align_corners=True    # matches cv2's pixel-center convention
        )

        front = front[0].permute(1, 2, 0).reshape(-1, 3).to(dtype=torch.uint8)
        print(f"front shape: {front.shape}")

        equirec = torch.zeros(equirect_height, equirect_width, 3, device=DEVICE, dtype=torch.uint8)
        equirec[:, :, :][front_mask] = front

        # equirec_arr = np.transpose(equirec_arr, (1, 2, 0))

        back_mask = z < 0
        print(f"back mask sum: {back_mask.sum()}")
        back_x = x[back_mask]
        back_y = y[back_mask]
        back_z = z[back_mask]

        back_xyz = torch.cat((back_x.unsqueeze(1), back_y.unsqueeze(1), back_z.unsqueeze(1)), axis=1)
        transposed_xyz = torch.transpose(back_xyz, 0, 1)
        rotated_xyz = torch.matmul(back_to_front_rotation,  transposed_xyz)
        back_xyz_transformed = back_to_front_translation.unsqueeze(1) + rotated_xyz
        back_x_tran = - back_xyz_transformed[0, :]
        back_y_tran = back_xyz_transformed[1, :]
        back_z_tran = back_xyz_transformed[2, :]

        r = torch.sqrt(back_x_tran**2 + back_y_tran**2)
        r[r<1e-6] = 1e-6
        theta = torch.atan2(r, torch.abs(back_z_tran))
        r_fisheye = 2 * theta / math.pi * (float(IMG_SHAPE[1]/2.0))
        back_map_x = K[0, 2] + back_x_tran/r*r_fisheye
        back_map_y = K[1, 2] + back_y_tran / r * r_fisheye

        back_map_x = back_map_x.reshape(IMG_SHAPE[0], IMG_SHAPE[1])
        back_map_y = back_map_y.reshape(IMG_SHAPE[0], IMG_SHAPE[1])

        # --- Replicate cv2.BORDER_WRAP ---
        # cv2 wraps x around width and y around height
        x_grid = torch.remainder(back_map_x, IMG_SHAPE[1])
        y_grid = torch.remainder(back_map_y, IMG_SHAPE[0])

        # --- Normalize pixel coords to [-1, 1] for grid_sample ---
        x_norm = 2.0 * x_grid / (IMG_SHAPE[1] - 1) - 1.0
        y_norm = 2.0 * y_grid / (IMG_SHAPE[0] - 1) - 1.0

        grid = torch.stack([x_norm, y_norm], dim=-1).unsqueeze(0)  # (1, H_out, W_out, 2)

        # h x w x c to b x c x h x w
        img2_t = img2_t.permute(2, 0, 1).unsqueeze(0)

        # print(img1_t.dtype)
        back = F.grid_sample(
            img2_t.float(), grid,
            mode='bicubic',            # 'bicubic' ~ cv2.INTER_CUBIC
            padding_mode='zeros', # irrelevant now, coords are pre-wrapped
            align_corners=True    # matches cv2's pixel-center convention
        )

        back = back[0].permute(1, 2, 0).reshape(-1, 3).to(dtype=torch.uint8)
        print(f"back shape: {back.shape}")

        equirec[:, :, :][back_mask] = back


        equirec_arr = equirec.cpu().detach().numpy()
        fig, ax = plt.subplots()
        ax.imshow(equirec_arr[:, :, [2, 1, 0]])
        plt.show()


        # imgs = [img1, img2]



if __name__ == "__main__":
    main()