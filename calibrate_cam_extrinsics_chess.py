
"""
RMS: 0.660166640915727
camera matrix:
 [[523.39510884   0.         959.49394175]
 [  0.         524.85636638 964.2452869 ]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.087575   -0.03389327  0.01168468 -0.00256208]

RMS: 0.43007790254895395
camera matrix:
 [[520.94868886   0.         953.17778948]
 [  0.         521.81516964 968.83095652]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.0821304  -0.02827705  0.00855254 -0.00161417]

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

IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-11-extrinsics-uncompr-rosbag2_2026_06_26-14_14_33"
# IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_3"

CHESSBOARD_SIZE = 0.023 # meters
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
DO_PLOTS = False
DO_PLOTS_UNDIST = False

# SELECTED_CAMERAS = [0, 1]
SELECTED_CAMERAS = [0, 1]

all_imgs = os.listdir(IMG_DIR)
all_imgs.sort()

for img_name in all_imgs:

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

    full_path = os.path.join(IMG_DIR, img_name)
    print(full_path)

    img_arr = cv2.imread(full_path)

    img_arr_half = img_arr.shape[1] // 2

    img1 = img_arr[:, 0:img_arr_half, :]
    img2 = img_arr[:, img_arr_half:, :]

    imgs = [img1, img2]


    if DO_PLOTS:
        fig, axes = plt.subplots(1, 2)
        fig.set_tight_layout(True)

    for i in SELECTED_CAMERAS:
        img = imgs[i]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # get checkerboard
        ret, corner_coordinates = cv2.findChessboardCorners(img_gray, (N_CORNERS_X, N_CORNERS_Y), cv2.CALIB_CB_ADAPTIVE_THRESH)

        if not ret:
            print(f"couldn't find chessboard camera {i}")
            if DO_PLOTS:
                axes[i].imshow(img[:, :, [2, 1, 0]])
            continue


        calibration_imgs[i].append(img.copy())
        calibration_img_names[i].append(full_path)

        reshaped_corner_coordinates = corner_coordinates.reshape((corner_coordinates.shape[0], corner_coordinates.shape[2]))
        uv_coords[i].append(reshaped_corner_coordinates.astype(np.float32))

        if DO_PLOTS:
            axes[i].imshow(img[:, :, [2, 1, 0]])
            axes[i].scatter(reshaped_corner_coordinates[:, 0], reshaped_corner_coordinates[:, 1], marker="x", color="green", s=CROSS_SIZE)
                
        # print(detections)
    if DO_PLOTS:
        plt.show()
        plt.close(fig)

    for j in range(len(uv_coords[0])):
        world_coords[0].append(CHESS_WORLD.copy().tolist())

    my_world_coords = np.expand_dims(np.array(world_coords[0]).astype(np.float32), -2)
    my_uv_coords_0 = np.expand_dims(np.array(uv_coords[0]).astype(np.float32), -2)
    my_uv_coords_1 = np.expand_dims(np.array(uv_coords[1]).astype(np.float32), -2)

    print(my_world_coords.shape)
    print(my_uv_coords_0.shape)
    print(my_uv_coords_1.shape)

    try:
        assert my_uv_coords_0.shape == my_uv_coords_1.shape
    except AssertionError:
        continue

    print(f"calculating camera calibration, camera idx: {i}")
    print("imgs:")
    [print(img_path) for img_path in calibration_img_names[i]]

    # rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(my_world_coords, my_uv_coords, (calibration_imgs[i][0].shape[1], calibration_imgs

    N_OK = len(my_uv_coords_0)


    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

    print(calibration_imgs[i][0].shape[1], calibration_imgs[i][0].shape[0])
    print(len(rvecs))
    print(rvecs[0].shape)


    R = np.eye(3)
    T = np.zeros(3,)

    """
        stereoCalibrate(objectPoints, imagePoints1, imagePoints2, K1, D1, K2, D2, imageSize[, R[, T[, rvecs[, tvecs[, flags[, criteria]]]]]]) -> retval, K1, D1, K2, D2, R, T, rve
    cs, tvecs
        .   @brief Performs stereo calibration
        .   
        .       @param objectPoints Vector of vectors of the calibration pattern points.
        .       @param imagePoints1 Vector of vectors of the projections of the calibration pattern points,
        .       observed by the first camera.
        .       @param imagePoints2 Vector of vectors of the projections of the calibration pattern points,
        .       observed by the second camera.
        .       @param K1 Input/output first camera intrinsic matrix:
        .       \f$\vecthreethree{f_x^{(j)}}{0}{c_x^{(j)}}{0}{f_y^{(j)}}{c_y^{(j)}}{0}{0}{1}\f$ , \f$j = 0,\, 1\f$ . If
        .       any of @ref fisheye::CALIB_USE_INTRINSIC_GUESS , @ref fisheye::CALIB_FIX_INTRINSIC are specified,
        .       some or all of the matrix components must be initialized.
        .       @param D1 Input/output vector of distortion coefficients \f$\distcoeffsfisheye\f$ of 4 elements.
        .       @param K2 Input/output second camera intrinsic matrix. The parameter is similar to K1 .
        .       @param D2 Input/output lens distortion coefficients for the second camera. The parameter is
        .       similar to D1 .
        .       @param imageSize Size of the image used only to initialize camera intrinsic matrix.
        .       @param R Output rotation matrix between the 1st and the 2nd camera coordinate systems.
        .       @param T Output translation vector between the coordinate systems of the cameras.
        .       @param rvecs Output vector of rotation vectors ( @ref Rodrigues ) estimated for each pattern view in the
        .       coordinate system of the first camera of the stereo pair (e.g. std::vector<cv::Mat>). More in detail, each
        .       i-th rotation vector together with the corresponding i-th translation vector (see the next output parameter
        .       description) brings the calibration pattern from the object coordinate space (in which object points are
        .       specified) to the camera coordinate space of the first camera of the stereo pair. In more technical terms,
        .       the tuple of the i-th rotation and translation vector performs a change of basis from object coordinate space
        .       to camera coordinate space of the first camera of the stereo pair.
        .       @param tvecs Output vector of translation vectors estimated for each pattern view, see parameter description
        .       of previous output parameter ( rvecs ).
        .       @param flags Different flags that may be zero or a combination of the following values:
        .       -    @ref fisheye::CALIB_FIX_INTRINSIC  Fix K1, K2? and D1, D2? so that only R, T matrices
        .       are estimated.
        .       -    @ref fisheye::CALIB_USE_INTRINSIC_GUESS  K1, K2 contains valid initial values of
        .       fx, fy, cx, cy that are optimized further. Otherwise, (cx, cy) is initially set to the image
        .       center (imageSize is used), and focal distances are computed in a least-squares fashion.
        .       -    @ref fisheye::CALIB_RECOMPUTE_EXTRINSIC  Extrinsic will be recomputed after each iteration
        .       of intrinsic optimization.
        .       -    @ref fisheye::CALIB_CHECK_COND  The functions will check validity of condition number.
        .       -    @ref fisheye::CALIB_FIX_SKEW  Skew coefficient (alpha) is set to zero and stay zero.
        .       -   @ref fisheye::CALIB_FIX_K1,..., @ref fisheye::CALIB_FIX_K4 Selected distortion coefficients are set to zeros and stay
        .       zero.
        .       @param criteria Termination criteria for the iterative optimization algorithm.
        
        
        
        stereoCalibrate(objectPoints, imagePoints1, imagePoints2, K1, D1, K2, D2, imageSize[, R[, T[, flags[, criteria]]]]) -> retval, K1, D1, K2, D2, R, T

    """

    for world_mult in [1, 10, 100]:
        print(world_mult)
        try:

            all_rets = cv2.fisheye.stereoCalibrate(my_world_coords * world_mult, my_uv_coords_0, my_uv_coords_1, Ks[0], Ds[0], Ks[1], Ds[1],
            (calibration_imgs[0][0].shape[1], calibration_imgs[0][0].shape[0]), R, T, flags=cv2.fisheye.CALIB_CHECK_COND | cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC | cv2.fisheye.CALIB_FIX_SKEW | cv2.fisheye.CALIB_FIX_K2 | cv2.fisheye.CALIB_FIX_K3 | cv2.fisheye.CALIB_FIX_K4 | cv2.fisheye.CALIB_FIX_K1 # Use this if your intrinsics are already known
            )

            print(all_rets)
            print(len(all_rets))

            ret, K1, D1, K2, D2, R, T, a, b = all_rets
            # print(R)
            print(R)
            print(T)
        except cv2.error as e:
            print(e)

"""
ouptut
(0.9863974350911984, array([[-8.96163060e+04, -8.34234045e+04,  1.39065263e+04],
       [ 0.00000000e+00, -8.53667580e+04,  5.10033510e+03],
       [ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]), array([  208.35369854, -1066.90110951,  2603.26187806, -2419.43298594]), array([[-3.96410047e+03, -1.49657115e+02, -3.70915855e+02],
       [ 0.00000000e+00, -3.83174847e+03,  1.35476545e+03],
       [ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]), array([ 27.21497005, -52.16405094,  44.56825308, -14.28716661]), array([[-0.81215121, -0.4240885 , -0.40069858],
       [-0.48643008,  0.8713979 ,  0.06365121],
       [ 0.32217415,  0.24660625, -0.91399627]]), array([113.09759366, -13.88305083, 252.21233908]), (array([[-1.00082539],
       [-2.51533627],
       [-2.73302969]]),), (array([[ 14.96025005],
       [  7.20559844],
       [257.76316615]]),))
"""

# cv::fisheye::stereoCalibrate 	( 	InputArrayOfArrays 	objectPoints,
#     InputArrayOfArrays 	imagePoints1,
#     InputArrayOfArrays 	imagePoints2,
#     InputOutputArray 	K1,
#     InputOutputArray 	D1,
#     InputOutputArray 	K2,
#     InputOutputArray 	D2,
#     Size 	imageSize,
#     OutputArray 	R,
#     OutputArray 	T,
#     OutputArrayOfArrays 	rvecs,
#     OutputArrayOfArrays 	tvecs,
#     int 	flags = fisheye::CALIB_FIX_INTRINSIC,
#     TermCriteria 	criteria = TermCriteria(TermCriteria::COUNT+TermCriteria::EPS, 100, DBL_EPSILON) )


# print("done calculating camera calibration")
# print("Found " + str(N_OK) + " valid images for calibration")
# print("\nRMS:", rms)
# print("camera matrix:\n", K)
# print("distortion coefficients: ", D.ravel())

#     for j in range(len(rvecs)):
#         img = calibration_imgs[i][j]
#         if DO_PLOTS_UNDIST:
#             fig, axes = plt.subplots(1, 2)
#             axes[0].imshow(img[:, :, [2, 1, 0]])
#             axes[0].set_xlabel("u")
#             axes[0].set_ylabel("v")
#             label = "re-projected corners"
#             for k in range(len(CHESS_WORLD)):
#                 imgpoints2, _ = cv2.fisheye.projectPoints(CHESS_WORLD[k].reshape((1, 1, 3)), rvecs[j], tvecs[j], K, D)
#                 imgpoints2 = imgpoints2.flatten()
#                 axes[0].scatter(imgpoints2[0], imgpoints2[1], marker="x", color="green", label = label, s=CROSS_SIZE)
#                 label = None

#             # uv_corners = transform_world_to_camera(newcameramtx, get_rot_from_euler(*rvecs[0].flatten()), tvecs[0], P_w)

#             axes[0].plot(my_uv_coords[j].reshape((-1, 2))[:, 0], my_uv_coords[j].reshape((-1, 2))[:, 1], 'r+', label="original_corners")
#             axes[0].set_title(f"Cam {i} w/ Intrinsics and Distortion Coefficients")
#             axes[0].legend()

#         img_dim = (img.shape[1], img.shape[0])

#         map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, img_dim, cv2.CV_16SC2)
#         undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
#         if DO_PLOTS_UNDIST:
#         # undistorted_image = undistorted_image[y:y+h, x:x+w]
#             axes[1].imshow(undistorted_img[:, :, [2, 1, 0]])
#             axes[1].set_title("Undistorted Image")
#             plt.show()
#             plt.close(fig)
