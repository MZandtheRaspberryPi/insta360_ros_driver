
"""
don't look good:
cam_idx 0
RMS: 0.5229540068393045
camera matrix:
 [[521.35896148   0.         955.94917325]
 [  0.         521.55810498 964.25474525]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.07544382 -0.02162714  0.0071692  -0.00204321]

second try, after removing some imgs. Let's try first though?
RMS: 0.5938105106512346
camera matrix:
 [[523.16245564   0.         949.78579237]
 [  0.         524.2414017  958.38163371]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.07149887 -0.01364544  0.00349411 -0.00182092]




look ok:
cam idx 1
RMS: 0.5213533334184552
camera matrix:
 [[524.52597527   0.         957.1131188 ]
 [  0.         523.06919916 964.83992242]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.07040753 -0.0148543   0.00355922 -0.00154401]
"""

CAM_0_K =  [[521.35896148,   0.,       955.94917325],
 [  0.,         521.55810498, 964.25474525],
 [  0. ,          0.,           1.        ]]
CAM_0_D = [ 0.07544382, -0.02162714,  0.0071692, -0.00204321]

CAM_1_K =  [[524.52597527,   0.,         957.1131188 ],
 [  0.,         523.06919916, 964.83992242],
 [  0.,           0.,          1.        ]]
CAM_1_D = [ 0.07040753, -0.0148543,   0.00355922, -0.00154401]


import time
import os

import matplotlib.pyplot as plt
import numpy as np
import cv2

Ks = np.array([CAM_0_K, CAM_1_K])
Ds = np.array([CAM_0_D, CAM_1_D])

IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected"
# IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_3"

CHESSBOARD_SIZE = 0.019 # meters
N_CORNERS_X = 6
N_CORNERS_Y = 9
CHESSBOARD_STARTING_POINT = np.array([0.0, 0.0])

x = np.array([i * CHESSBOARD_SIZE for i in range(0, N_CORNERS_X)]) 
y = np.array([i * CHESSBOARD_SIZE for i in range(0, N_CORNERS_Y)])
xv, yv = np.meshgrid(x, y)
reshaped_xv = xv.reshape((xv.shape[0] * xv.shape[1], 1))
reshaped_yv = yv.reshape((yv.shape[0] * yv.shape[1], 1))
CHESS_WORLD = np.hstack((reshaped_xv, reshaped_yv, np.zeros((reshaped_xv.shape[0], 1))))

CROSS_SIZE = 30

DO_PLOTS_UNDIST = True

SELECTED_CAMERAS = [0, 1]
SELECTED_IMGS = ["img_raw_0000164_54.68989539146423.png", "img_raw_0000360_120.11098408699036.png"]

calibration_img_names = []
calibration_imgs = []
world_coords = []
uv_coords = []
n_cam = 2
for i in range(n_cam):
    calibration_imgs.append([])
    world_coords.append([])
    uv_coords.append([])
    calibration_img_names.append([])

all_imgs = os.listdir(IMG_DIR)
all_imgs.sort()

for img_name in all_imgs:

    # if img_name not in SELECTED_IMGS:
    #     continue

    full_path = os.path.join(IMG_DIR, img_name)
    print(full_path)

    img_arr = cv2.imread(full_path)

    img_arr_half = img_arr.shape[1] // 2

    img1 = img_arr[:, 0:img_arr_half, :]
    img2 = img_arr[:, img_arr_half:, :]

    imgs = [img1, img2]

    for i in SELECTED_CAMERAS:
        img = imgs[i]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # get checkerboard
        ret, corner_coordinates = cv2.findChessboardCorners(img_gray, (N_CORNERS_X, N_CORNERS_Y))

        if not ret:
            print(f"couldn't find chessboard camera {i}")
            continue


        calibration_imgs[i].append(img.copy())
        calibration_img_names[i].append(full_path)

        reshaped_corner_coordinates = corner_coordinates.reshape((corner_coordinates.shape[0], corner_coordinates.shape[2]))
        uv_coords[i].append(reshaped_corner_coordinates.astype(np.float32))

                
        # print(detections)


for i in SELECTED_CAMERAS:

    if len(uv_coords[i]) == 0:
        continue

    for j in range(len(uv_coords[i])):
        world_coords[i].append(CHESS_WORLD.copy().tolist())

    my_world_coords = np.expand_dims(np.array(world_coords[i]).astype(np.float32), -2)
    my_uv_coords = np.expand_dims(np.array(uv_coords[i]).astype(np.float32), -2)   
    
    K = Ks[i]
    D = Ds[i]
    N_OK = len(my_uv_coords)
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

            # (calibration_imgs[i][0].shape[1], calibration_imgs[i][0].shape[0]),

    for j in range(N_OK):
        rvec = np.zeros((3), dtype=np.float32)
        tvec = np.zeros((3), dtype=np.float32)
        for _ in [my_world_coords[j], my_uv_coords[j], K, D, rvec, tvec]:
            print(_)
        rets = cv2.fisheye.solvePnP(my_world_coords[j], my_uv_coords[j], K, D, rvec, tvec)
        rvecs[j] = rvec
        tvecs[j] = tvec


    for j in range(len(rvecs)):
        img = calibration_imgs[i][j]
        if DO_PLOTS_UNDIST:
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(img[:, :, [2, 1, 0]])
            axes[0].set_xlabel("u")
            axes[0].set_ylabel("v")
            label = "re-projected corners"
            for k in range(len(CHESS_WORLD)):
                imgpoints2, _ = cv2.fisheye.projectPoints(CHESS_WORLD[k].reshape((1, 1, 3)), rvecs[j], tvecs[j], K, D)
                imgpoints2 = imgpoints2.flatten()
                axes[0].scatter(imgpoints2[0], imgpoints2[1], marker="x", color="green", label = label, s=CROSS_SIZE)
                label = None

            axes[0].plot(my_uv_coords[j].reshape((-1, 2))[:, 0], my_uv_coords[j].reshape((-1, 2))[:, 1], 'r+', label="original_corners")
            axes[0].set_title(f"Cam {i} w/ Intrinsics and Distortion Coefficients")
            axes[0].legend()

        img_dim = (img.shape[1], img.shape[0])

        balance = 0.4
        new_k = K.copy()
        new_k[0,0]=new_k[0,0] * balance
        new_k[1,1]=new_k[1,1] * balance
        dim2 = (int(balance * img_dim[0]), int(balance*img_dim[1]))

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_k, img_dim, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        if DO_PLOTS_UNDIST:
        # undistorted_image = undistorted_image[y:y+h, x:x+w]
            axes[1].imshow(undistorted_img[:, :, [2, 1, 0]])
            axes[1].set_title("Undistorted Image")
            plt.show()
            plt.close(fig)