
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

CAM_0_K =  [[523.39510884,   0.,      959.49394175],
 [  0.,         524.85636638, 964.2452869],
 [  0. ,          0.,           1.        ]]
CAM_0_D = [0.087575,   -0.03389327,  0.01168468, -0.00256208]

CAM_1_K =  [[520.94868886,   0.,        953.17778948 ],
 [  0.,         521.81516964, 968.83095652],
 [  0.,           0.,          1.        ]]
CAM_1_D = [  0.0821304,  -0.02827705,  0.00855254, -0.00161417]

CALIBRATION_DIM = (1920, 1920)

import time
import os

import matplotlib.pyplot as plt
import numpy as np
import cv2

Ks = np.array([CAM_0_K, CAM_1_K])
Ds = np.array([CAM_0_D, CAM_1_D])

IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/spot-day-out-rgb"

DO_PLOTS_UNDIST = True

SELECTED_CAMERAS = [1]
SELECTED_IMGS = ["img_raw_0000001_0.03801465034484863.png"]

calibration_img_names = []
calibration_imgs = []
n_cam = 2
for i in range(n_cam):
    calibration_imgs.append([])
    calibration_img_names.append([])

all_imgs = os.listdir(IMG_DIR)
all_imgs.sort()

for img_name in all_imgs:

    if img_name not in SELECTED_IMGS:
        continue

    full_path = os.path.join(IMG_DIR, img_name)

    img_arr = cv2.imread(full_path)

    img_arr_half = img_arr.shape[1] // 2

    img1 = img_arr[:, 0:img_arr_half, :]
    img2 = img_arr[:, img_arr_half:, :]

    imgs = [img1, img2]

    for i in SELECTED_CAMERAS:
        img = imgs[i]
        calibration_imgs[i].append(img.copy())
        calibration_img_names[i].append(full_path)

for i in SELECTED_CAMERAS:

    K = Ks[i]
    D = Ds[i]

    for j in range(len(calibration_imgs[i])):
        img = calibration_imgs[i][j]
        full_path = calibration_img_names[i][j]
        print(full_path)
        fig, axes = plt.subplots(1, 2)
        axes[0].imshow(img[:, :, [2, 1, 0]])
        axes[0].set_xlabel("u")
        axes[0].set_ylabel("v")
        
        axes[0].set_title(f"Cam {i} Img")

        img_dim = (img.shape[1], img.shape[0])

        assert img_dim[0]/img_dim[1] == CALIBRATION_DIM[0]/CALIBRATION_DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
        # if not dim2:
        #     dim2 = dim1
        # if not dim3:
        #     dim3 = dim1
        scaled_K = K * img_dim[0] / CALIBRATION_DIM[0]  # The values of K is to scale with image dimension.
        scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

        # balance = 0.4
        # new_k = K.copy()
        # new_k[0,0]=new_k[0,0] * balance
        # new_k[1,1]=new_k[1,1] * balance
        # dim2 = (int(balance * img_dim[0]), int(balance*img_dim[1]))

        # map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_k, img_dim, cv2.CV_16SC2)
        # undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        # auto crop
        # map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), scaled_K, img_dim, cv2.CV_16SC2)
        # undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
        dim2 = img_dim
        dim3 = dim2
        balance = 0.0
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, R=np.eye(3), balance=balance, fov_scale=1.5)
        print(f"K: {K}")
        print(f"scaled_K: {scaled_K}")
        print(f"new_K: {new_K}")
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

# estimateNewCameraMatrixForUndistortRectify(...)
#     estimateNewCameraMatrixForUndistortRectify(K, D, image_size, R[, P[, balance[, new_size[, fov_scale]]]]) -> P
#     .   @brief Estimates new camera intrinsic matrix for undistortion or rectification.
#     .   
#     .       @param K Camera intrinsic matrix \f$\cameramatrix{K}\f$.
#     .       @param image_size Size of the image
#     .       @param D Input vector of distortion coefficients \f$\distcoeffsfisheye\f$.
#     .       @param R Rectification transformation in the object space: 3x3 1-channel, or vector: 3x1/1x3
#     .       1-channel or 1x1 3-channel
#     .       @param P New camera intrinsic matrix (3x3) or new projection matrix (3x4)
#     .       @param balance Sets the new focal length in range between the min focal length and the max focal
#     .       length. Balance is in range of [0, 1].
#     .       @param new_size the new size
#     .       @param fov_scale Divisor for new focal length.


# initUndistortRectifyMap(...)
#     initUndistortRectifyMap(K, D, R, P, size, m1type[, map1[, map2]]) -> map1, map2
#     .   @brief Computes undistortion and rectification maps for image transform by #remap. If D is empty zero
#     .       distortion is used, if R or P is empty identity matrixes are used.
#     .   
#     .       @param K Camera intrinsic matrix \f$\cameramatrix{K}\f$.
#     .       @param D Input vector of distortion coefficients \f$\distcoeffsfisheye\f$.
#     .       @param R Rectification transformation in the object space: 3x3 1-channel, or vector: 3x1/1x3
#     .       1-channel or 1x1 3-channel
#     .       @param P New camera intrinsic matrix (3x3) or new projection matrix (3x4)
#     .       @param size Undistorted image size.
#     .       @param m1type Type of the first output map that can be CV_32FC1 or CV_16SC2 . See #convertMaps
#     .       for details.
#     .       @param map1 The first output map.
#     .       @param map2 The second output map.


        # # claude
        # # Compute the new camera matrix, balancing FOV vs cropping (0 = crop tightly,
        # # 1 = keep all pixels but with more black borders)
        # new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
        #     K, D, img_dim, np.eye(3), balance=0.0
        # )

        # # Precompute the undistortion maps
        # map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        #     K, D, np.eye(3), new_K, img_dim, cv2.CV_16SC2
        # )

        # # Apply the remap to get the undistorted image
        # undistorted_img = cv2.remap(
        #     img, map1, map2, interpolation=cv2.INTER_LINEAR,
        #     borderMode=cv2.BORDER_CONSTANT
        # )

        # print(f"{img.shape}")
        # print(f"{scaled_K.shape}")
        # print(f"{D.shape}")
        # print(f"{scaled_K.shape}")
        # print(f"{img_dim}")
        # undistorted_img = cv2.fisheye.undistortImage(img, K, D)
        

        # undistorted_image = undistorted_image[y:y+h, x:x+w]
        axes[1].imshow(undistorted_img[:, :, [2, 1, 0]])
        axes[1].set_title(f"Cam {i} Undistorted Img")
        plt.show()
        plt.close(fig)