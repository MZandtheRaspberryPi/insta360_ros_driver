# download and build april tag repo
# https://github.com/AprilRobotics/apriltag
# cmake -B build -DCMAKE_BUILD_TYPE=Release
# export PYTHONPATH=/home/developer/apriltag/build:$PYTHONPATH
# run

import time
import os

from apriltag import apriltag
import matplotlib.pyplot as plt
import numpy as np
import cv2

IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/calibration_imgs_selection_bigger"
# IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_3"

FIDUCIAL_MARKER_SIZE = 0.074 # meters
DETECTOR = apriltag("tagStandard41h12")

WORLD_CORNERS_AND_CENTER_POS = np.zeros((5,3), np.float32)
WORLD_CORNERS_AND_CENTER_POS[0] = [-FIDUCIAL_MARKER_SIZE/2, -FIDUCIAL_MARKER_SIZE/2, 0] #top left
WORLD_CORNERS_AND_CENTER_POS[1] = [FIDUCIAL_MARKER_SIZE/2, -FIDUCIAL_MARKER_SIZE/2, 0] #top right
WORLD_CORNERS_AND_CENTER_POS[2] = [-FIDUCIAL_MARKER_SIZE/2, FIDUCIAL_MARKER_SIZE/2, 0] #bottom left
WORLD_CORNERS_AND_CENTER_POS[3] = [FIDUCIAL_MARKER_SIZE/2, FIDUCIAL_MARKER_SIZE/2, 0] #bottom right
WORLD_CORNERS_AND_CENTER_POS[4] = [0, 0, 0] # middle

CROSS_SIZE = 30
DO_PLOTS = True
DO_PLOTS_UNDIST = True

def transform_world_to_camera(K, R, t, world_coords):
    """
    Args:
        K: np.array with shape (3, 3), camera intrinsics matrix.
        R: np.array with shape (3, 3), camera rotation.
        t: np.array with shape (3, ) or (3, 1), camera translation.
        world_coords: np.array with shape (N, 3), cartesian coordinates (X, Y, Z)
            in world frame to transform into camera pixel space.
    Return:
        uv: np.array with shape (N, 2), with (u, v) coordinates of that are
            the projections of the the world_coords on the image plane.
    """
    uv = []
    for i in range(world_coords.shape[0]):
        homog_pix = K.dot(R.dot(world_coords[i, :]) + t)
        uv_pnt = np.array([homog_pix[0] / homog_pix[2], homog_pix[1] / homog_pix[2]])
        uv.append(uv_pnt)
    uv = np.vstack(uv)
    return uv

def get_x_rotation(rx: float):

    return np.array([[1, 0, 0],
                    [0, np.cos(rx), -np.sin(rx)],
                    [0, np.sin(rx), np.cos(rx)]])

def get_y_rotation(ry: float):

    return np.array([[np.cos(ry), 0, np.sin(ry)],
                    [0, 1, 0],
                    [-np.sin(ry), 0, np.cos(ry)]]) 


def get_z_rotation(rz: float):

    return np.array([[np.cos(rz), -np.sin(rz), 0],
                    [np.sin(rz), np.cos(rz), 0],
                    [0, 0, 1]])

def get_rot_from_euler(rx, ry, rz):


    x = get_x_rotation(rx)
    y = get_y_rotation(ry)
    z = get_z_rotation(rz)

    return z @ y @ x


calibration_imgs = []
world_coords = []
uv_coords = []
n_cam = 2
for i in range(n_cam):
    calibration_imgs.append([])
    world_coords.append([])
    uv_coords.append([])


for img_name in os.listdir(IMG_DIR):
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

    for i in range(2):
        img = imgs[i]
        print(img.shape)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detections = DETECTOR.detect(img_gray)

        if len(detections) == 0:
            if DO_PLOTS:
                axes[i].imshow(img[:, :, [2, 1, 0]])
            continue


        calibration_imgs[i].append(img.copy())
        for j in range(len(detections)):
            detect = detections[j]
            uv = np.vstack([detect["lb-rb-rt-lt"][[3, 2, 0, 1], :], detect["center"]]).astype(np.float32)
            uv_coords[i].append(uv.tolist())
            if DO_PLOTS:
                corners = np.reshape(np.array([detect["lb-rb-rt-lt"]]), (4,1,2)).astype(np.int32)
                cv2.drawContours(img, (corners,), -1, (0, 0, 255), 1)
                axes[i].imshow(img[:, :, [2, 1, 0]])

                axes[i].scatter(detect["center"][0], detect["center"][1], marker="x", color="red", s=CROSS_SIZE)
                axes[i].scatter(detect["lb-rb-rt-lt"][:, 0], detect["lb-rb-rt-lt"][:, 1], marker="x", color="green", s=CROSS_SIZE)
                
        # print(detections)
    if DO_PLOTS:
        plt.show()
        plt.close(fig)


# for i in range(n_cam):
for i in range(1, n_cam):

    for j in range(len(uv_coords[i])):
        world_coords[i].append(WORLD_CORNERS_AND_CENTER_POS.copy().tolist())

    my_world_coords = np.array(world_coords[i]).astype(np.float32)
    my_uv_coords = np.array(uv_coords[i]).astype(np.float32)

    raise NotImplementedError("Not yet done...")
