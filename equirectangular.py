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

CAM_0_K =  [[523.39510884,   0.,      959.49394175],
 [  0.,         524.85636638, 964.2452869],
 [  0. ,          0.,           1.        ]]
CAM_0_D = [0.087575,   -0.03389327,  0.01168468, -0.00256208]

CAM_1_K =  [[520.94868886,   0.,        953.17778948 ],
 [  0.,         521.81516964, 968.83095652],
 [  0.,           0.,          1.        ]]
CAM_1_D = [  0.0821304,  -0.02827705,  0.00855254, -0.00161417]

Ks = np.array([CAM_0_K, CAM_1_K])
Ds = np.array([CAM_0_D, CAM_1_D])

def spherical2equirect(sp_coords: np.ndarray,
                       width: int,
                       height: int)-> np.ndarray:
    """
    Args:
        sp_coords (np.ndarray): Spherical coordinates (theta, phi, rho)
        width (int): Width of the equirectangular image
        height (int): Height of the equirectangular image

    Returns:
        np.ndarray: Equirectangular coordinates (x, y)
    """

    rho, theta, phi = sp_coords[..., 0], sp_coords[..., 1], sp_coords[..., 2]
    x = (theta / (2 * np.pi) + 0.5) * (width)
    y = (phi / (np.pi) + 0.5) * (height)

    return np.stack([x, y]).transpose(2, 1, 0) # (width, height, 2)

def get_camera_matrix(FOV: float, width: int, height: int) -> np.ndarray:
    """

    Computes the intrinsic camera matrix from the given camera
    field of view (FOV) and image/window dimensions.

    Args:
        FOV (float): Field of view in radians
        width (int): Image/window width
        height (int): Image/window height

    Returns:
        K (np.ndarray): 3x3 matrix representing the intrinsic camera matrix
    """

    f = 0.5 * width / np.tan(0.5 * FOV)
    cx = (width) / 2.0
    cy = (height) / 2.0

    K = np.array([
            [f, 0, cx],
            [0, f, cy],
            [0, 0, 1]]).astype(np.float32)

    return K

def get_extrinsic_matrix(theta:float, phi:float):

    # Default
    elevation_vector = np.array([0.0, theta, 0.0], np.float32)
    azimuth_vector = np.array([phi, 0.0, 0.0], np.float32)

    # Use Rodrigues' formula to convert the
    # angle vector (simulatenous) to rotation matrix
    R1, _ = cv2.Rodrigues(elevation_vector)
    R2, _ = cv2.Rodrigues(np.dot(R1, azimuth_vector))

    R = R2 @ R1
    return R

def camera_to_world(points: np.ndarray, K: np.ndarray, R:np.ndarray) -> np.ndarray:
    """

    Transforms the given 3D points from camera coordinates to world coordinates

    Args:
        points (np.ndarray): 3D points in homogeneous camera coordinates
        K (np.ndarray): 3x3 matrix representing the intrinsic camera matrix
        R (np.ndarray): 3x3 matrix representing the extrinsic camera matrix (rotation)

    Returns:
        world_points (np.ndarray): 3D points in world coordinates

    """

    K_inv = np.linalg.inv(K)

    world_points = (points @ K_inv.T) @ R.T
    return world_points


def cartesian_to_spherical(points: np.ndarray) -> np.ndarray:
    """
    Converts the given 3D points from cartesian coordinates to spherical coordinates

    Args:
        points (np.ndarray): 3D points in cartesian coordinates

    Returns:
        sp_coords (np.ndarray): 3D points in spherical coordinates (rho, theta, phi)
    """

    assert points.shape[-1] == 3, "Input should have 3 (X, Y, Z) components"

    x, y, z = points[..., 0], points[..., 1], points[..., 2]

    # Distance of points from the origin
    rho = np.linalg.norm(points, axis=-1)

    # Normalize the points on the sphere of the above radius
    # to get the points on the unit sphere
    x /= rho
    y /= rho
    z /= rho

    # Elevation angle (aka latitude)
    phi = np.arcsin(y)

    # Azimuthal angle (aka longitude)
    theta = np.arctan2(x, z)

    # return np.stack([rho, theta, phi], axis=-1)
    return np.stack([rho, theta, phi]).T

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

        # now to cartesian world coordinates

        x = 1.0 * torch.cos(elevation) * torch.sin(azimuth)
        y = 1.0 * torch.sin(elevation)
        z = 1.0 * torch.cos(elevation) * torch.cos(azimuth)

        # z[torch.logical_and(z<1e-3, z > 0.0)] = 1e-3
        # z[torch.logical_and(z>-1e-3, z < 0.0)] = -1e-3

        front_mask = z >= 0.0
        front_x = x[front_mask]
        front_y = y[front_mask]
        front_z = z[front_mask]

        print(f"front_x shape: {front_x.shape}")
        print(f"front_z min: {front_z.min()} max: {front_z.max()} avg: {front_z.mean()}")

        # Rt = torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=torch.float32, device=DEVICE)

        # xyz = torch.cat((front_x.unsqueeze(0), front_y.unsqueeze(0), front_z.unsqueeze(0), torch.ones_like(front_z).unsqueeze(0)), dim=0)
        # uv = K @ (Rt @ xyz)
        # uv = torch.transpose(uv, 0, 1)
        # # uv = (xyz @ Rt) @ torch.transpose(K, 0, 1)
        # print(uv.shape)
        # print(uv[:5, 0])
        # print(uv[:5, 1])
        # print(uv[:5, 2])
        # uv[:, 0] /= uv[:, 2] 
        # uv[:, 1] /= uv[:, 2] 
        # uv[:, 2] /= uv[:, 2] 
        # print(uv[:5, 0])
        # print(uv[:5, 1])
        # print(uv[:5, 2])

        # radius of normalized fisheye coord
        r = torch.sqrt(front_x**2 + front_y**2)
        r[r<1e-6] = 1e-6

        theta = torch.atan2(r, torch.abs(front_z))

        r_fisheye = 2 * theta / math.pi * (float(IMG_SHAPE[1])/2.0)
        K = Ks[1]
        front_map_x = K[0, 2] + front_x/r * r_fisheye
        front_map_y = K[1, 2] + front_y / r * r_fisheye

        # lon = torch.atan2(front_z, front_x)
        # lat = torch.atan2()

        x_grid = front_map_x.reshape(IMG_SHAPE[0], IMG_SHAPE[1])
        y_grid = front_map_y.reshape(IMG_SHAPE[0], IMG_SHAPE[1])

        # front_map_x = uv[:, 0].reshape(IMG_SHAPE[0], IMG_SHAPE[1])
        # front_map_y = uv[:, 1].reshape(IMG_SHAPE[0], IMG_SHAPE[1])

        # --- Normalize pixel coords to [-1, 1] for grid_sample ---
        x_norm = 2.0 * x_grid / (IMG_SHAPE[1] - 1) - 1.0
        y_norm = 2.0 * y_grid / (IMG_SHAPE[0] - 1) - 1.0

        grid = torch.stack([x_norm, y_norm], dim=-1).unsqueeze(0)  # (1, H_out, W_out, 2)

        # h x w x c to b x c x h x w
        img2_t = img2_t.permute(2, 0, 1).unsqueeze(0)

        # print(img1_t.dtype)
        front = F.grid_sample(
            img2_t.float(), grid,
            mode='bilinear',
            padding_mode='zeros',
            align_corners=True 
        )

        front = front[0].permute(1, 2, 0).reshape(-1, 3).to(dtype=torch.uint8)
        print(f"front shape: {front.shape}")

        equirec = torch.zeros(equirect_height, equirect_width, 3, device=DEVICE, dtype=torch.uint8)
        equirec[front_mask] = front

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
        K = Ks[0]
        back_map_x = K[0, 2] + back_x_tran/r*r_fisheye
        back_map_y = K[1, 2] + back_y_tran / r * r_fisheye

        x_grid = back_map_x.reshape(IMG_SHAPE[0], IMG_SHAPE[1])
        y_grid = back_map_y.reshape(IMG_SHAPE[0], IMG_SHAPE[1])

        # --- Normalize pixel coords to [-1, 1] for grid_sample ---
        x_norm = 2.0 * x_grid / (IMG_SHAPE[1] - 1) - 1.0
        y_norm = 2.0 * y_grid / (IMG_SHAPE[0] - 1) - 1.0

        grid = torch.stack([x_norm, y_norm], dim=-1).unsqueeze(0)  # (1, H_out, W_out, 2)

        # h x w x c to b x c x h x w
        img1_t = img1_t.permute(2, 0, 1).unsqueeze(0)

        # print(img1_t.dtype)
        back = F.grid_sample(
            img1_t.float(), grid,
            mode='bilinear',            # 'bicubic' ~ cv2.INTER_CUBIC
            padding_mode='zeros', # irrelevant now, coords are pre-wrapped
            align_corners=True    # matches cv2's pixel-center convention
        )

        back = back[0].permute(1, 2, 0).reshape(-1, 3).to(dtype=torch.uint8)
        print(f"back shape: {back.shape}")

        equirec[back_mask] = back

        # generate perspective images from equirectangular

        # 100 degree fov
        fov = 130 * math.pi / 180

        azi = (0.0, math.pi)
        ele = (0.0, 0.0)

        new_imgs = []

        for i in range(len(azi)):


            azimuth = azi[i]
            elevation = ele[i]

            img_height, img_width = equirec.shape[0], equirec.shape[0]
            # Compute the intrinsic camera matrix
            K = get_camera_matrix(fov, img_width, img_height)

            # Compute the extrinsic matrix
            R = get_extrinsic_matrix(azimuth, elevation)

            # image grid
            x, y = np.meshgrid(np.arange(img_width), np.arange(img_height))

            # Convert the image grid to homogeneous coordinates
            z = np.ones_like(x)
            xyz = np.concatenate([x[..., None], y[..., None], z[..., None]], axis=-1)

            # Convert the image grid to world coordinates
            world_coords = camera_to_world(xyz, K, R)

            sp_coords = cartesian_to_spherical(world_coords)

            XY = spherical2equirect(sp_coords, img_width, img_height)

            grid = torch.tensor(XY, device=DEVICE, dtype=torch.float32).unsqueeze(0)
            print(f"grid shape: {grid.shape}")

            grid[:, :, :, 0] = 2.0 * grid[:, :, :, 0] / (img_width) - 1.0
            grid[:, :, :, 1] = 2.0 * grid[:, :, :, 1] / (img_height) - 1.0


            equirec_arr = equirec.cpu().detach().numpy()

            equirec_p = equirec.permute(2, 0, 1).unsqueeze(0)

            print(f"equirec_p shape: {equirec_p.shape}")

            # print(img1_t.dtype)
            new = F.grid_sample(
                equirec_p.float(), grid,
                mode='bilinear',            # 'bicubic' ~ cv2.INTER_CUBIC
                padding_mode='zeros', # irrelevant now, coords are pre-wrapped
                align_corners=True    # matches cv2's pixel-center convention
            )

            print(f"new shape: {new.shape}")

            new = new[0].permute(1, 2, 0).to(dtype=torch.uint8)


            new_arr = new.cpu().detach().numpy()

            new_imgs.append(new_arr)

        fig = plt.figure()

        gs = fig.add_gridspec(3, 3)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1:, :2])
        ax4 = fig.add_subplot(gs[0, 2])
        ax5 = fig.add_subplot(gs[1, 2])

        ax1.set_title("Fisheye Img0")
        ax1.imshow(img1[:, :, [2, 1, 0]])
        ax2.set_title("Fisheye Img1")
        ax2.imshow(img2[:, :, [2, 1, 0]])
        ax3.set_title("Equirectangular")
        ax3.imshow(equirec_arr[:, :, [2, 1, 0]])
        ax4.set_title(f"Persp. FOV {round(180 * fov / math.pi, 0)}")
        ax4.imshow(new_imgs[0][:, :, [2, 1, 0]])
        ax5.set_title(f"Persp. FOV {round(180 * fov / math.pi, 0)}")
        ax5.imshow(new_imgs[1][:, :, [2, 1, 0]])
        fig.tight_layout()
        plt.show()


        # imgs = [img1, img2]



if __name__ == "__main__":
    main()