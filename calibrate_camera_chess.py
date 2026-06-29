
"""
Traceback (most recent call last):
  File "/home/developer/ros_ws/src/rpl_nav/scripts/calibrate_camera_chess.py", line 176, in <module>
    cv2.fisheye.calibrate(
cv2.error: OpenCV(4.5.4) ./modules/calib3d/src/fisheye.cpp:1449: error: (-3:Internal error) CALIB_CHECK_COND - Ill-conditioned matrix for input array 5 in function 'CalibrateExtrinsics'

means one of the photos isn't good. Check if chessboard too close to the edge...


developer@student-AORUS-5-KB:~/ros_ws$ python3 src/rpl_nav/scripts/calibrate_camera_chess.py 
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000000_0.0.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000036_11.992810487747192.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000049_16.167787551879883.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000086_28.68902611732483.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000098_32.629414558410645.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000138_45.93765592575073.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000150_49.88924980163574.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000164_54.68989539146423.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000188_62.56792640686035.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000206_68.90788221359253.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000235_78.3499207496643.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000248_82.69154119491577.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000271_90.59308099746704.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000299_99.64325737953186.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000319_106.48441553115845.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000330_110.06968569755554.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000352_117.38823342323303.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000360_120.11098408699036.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000373_124.38402581214905.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000386_128.77284693717957.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000400_133.34619879722595.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000461_154.33117055892944.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000471_156.9809112548828.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000483_161.16517853736877.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000506_168.82461833953857.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000526_175.81893301010132.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000534_178.20086908340454.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000563_187.85803389549255.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000572_190.73891687393188.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000601_200.49730348587036.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000654_218.61681413650513.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000706_235.46884059906006.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000720_240.2544059753418.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000725_241.7702453136444.png
couldn't find chessboard camera 1
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000754_251.40666007995605.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000775_258.6123855113983.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000786_262.2357859611511.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000797_266.54165530204773.png
couldn't find chessboard camera 0
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000822_274.1302971839905.png
couldn't find chessboard camera 0
(20, 54, 1, 3)
(20, 54, 1, 2)
calculating camera calibration, camera idx: 0
imgs:
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000138_45.93765592575073.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000150_49.88924980163574.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000164_54.68989539146423.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000188_62.56792640686035.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000206_68.90788221359253.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000235_78.3499207496643.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000248_82.69154119491577.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000271_90.59308099746704.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000299_99.64325737953186.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000319_106.48441553115845.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000330_110.06968569755554.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000526_175.81893301010132.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000534_178.20086908340454.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000563_187.85803389549255.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000572_190.73891687393188.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000601_200.49730348587036.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000654_218.61681413650513.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000706_235.46884059906006.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000720_240.2544059753418.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000725_241.7702453136444.png
(3, 3)
(4, 1)
1920 1920
20
(1, 1, 3)
done calculating camera calibration
Found 20 valid images for calibration

RMS: 0.5229540068393045
camera matrix:
 [[521.35896148   0.         955.94917325]
 [  0.         521.55810498 964.25474525]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.07544382 -0.02162714  0.0071692  -0.00204321]
(19, 54, 1, 3)
(19, 54, 1, 2)
calculating camera calibration, camera idx: 1
imgs:
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000000_0.0.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000036_11.992810487747192.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000049_16.167787551879883.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000086_28.68902611732483.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000098_32.629414558410645.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000352_117.38823342323303.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000360_120.11098408699036.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000373_124.38402581214905.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000386_128.77284693717957.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000400_133.34619879722595.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000461_154.33117055892944.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000471_156.9809112548828.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000483_161.16517853736877.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000506_168.82461833953857.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000754_251.40666007995605.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000775_258.6123855113983.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000786_262.2357859611511.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000797_266.54165530204773.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4_selected/img_raw_0000822_274.1302971839905.png
(3, 3)
(4, 1)
1920 1920
19
(1, 1, 3)
done calculating camera calibration
Found 19 valid images for calibration

RMS: 0.5213533334184552
camera matrix:
 [[524.52597527   0.         957.1131188 ]
 [  0.         523.06919916 964.83992242]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.07040753 -0.0148543   0.00355922 -0.00154401]


"""


"""
cali june 26 on cali9

cam0:
imgs:
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0000857_142.6593039035797.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0000929_154.72589492797852.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0000968_161.20422887802124.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001022_170.2128026485443.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001042_173.53025913238525.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001096_182.5503125190735.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001151_191.6538107395172.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001196_199.42094779014587.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001216_202.49955487251282.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001277_212.8973696231842.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001301_216.7310266494751.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001315_219.04678177833557.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001337_222.78635168075562.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001409_234.71597456932068.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-9-selected-cam-0/img_raw_0001415_235.74097895622253.png
done calculating camera calibration
Found 15 valid images for calibration

RMS: 0.6525323168594677
camera matrix:
 [[518.62533526   0.         952.54933439]
 [  0.         520.07344497 963.67529999]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.0927486  -0.04045851  0.01693481 -0.00386533]



camera1: 
RMS: 0.6984141778284092
camera matrix:
 [[524.08354498   0.         955.54902783]
 [  0.         525.27323207 963.4945584 ]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.08178777 -0.01882028  0.00116621 -0.00111479]



with new firmware, jun 26

camera0:
imgs:
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0000816_27.188166618347168.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0000841_28.010162591934204.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0000889_29.616190195083618.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0000947_31.54619312286377.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0000959_31.96018958091736.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001054_35.144211292266846.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001065_35.49222373962402.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001143_38.08822989463806.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001175_39.160234212875366.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001219_40.64425182342529.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001260_42.0422523021698.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001277_42.58826208114624.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001298_43.25825595855713.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001308_43.638261795043945.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001318_43.93427872657776.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001365_45.48627209663391.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001402_46.73428273200989.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected/img_raw_0001447_48.23029351234436.png
(3, 3)
(4, 1)
1920 1920
18
(1, 1, 3)
done calculating camera calibration
Found 18 valid images for calibration

RMS: 0.660166640915727
camera matrix:
 [[523.39510884   0.         959.49394175]
 [  0.         524.85636638 964.2452869 ]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.087575   -0.03389327  0.01168468 -0.00256208]

camera1:
imgs:
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000008_0.22800922393798828.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000060_2.0020172595977783.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000079_2.59602689743042.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000143_4.726037979125977.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000161_5.314035892486572.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000240_7.95805287361145.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000291_9.664052963256836.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000319_10.596052408218384.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000332_11.070089101791382.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000404_13.452085256576538.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000425_14.132076025009155.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000496_16.502095222473145.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000576_19.172114849090576.png
/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-1-selected/img_raw_0000644_21.46013832092285.png
(3, 3)
(4, 1)
1920 1920
14
(1, 1, 3)
done calculating camera calibration
Found 14 valid images for calibration

RMS: 0.43007790254895395
camera matrix:
 [[520.94868886   0.         953.17778948]
 [  0.         521.81516964 968.83095652]
 [  0.           0.           1.        ]]
distortion coefficients:  [ 0.0821304  -0.02827705  0.00855254 -0.00161417]

"""

import time
import os

import matplotlib.pyplot as plt
import numpy as np
import cv2

IMG_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/rgb-cali-10-cam-0-selected"
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
DO_PLOTS_UNDIST = True

# SELECTED_CAMERAS = [0, 1]
SELECTED_CAMERAS = [0]

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


# for i in range(n_cam):
for i in SELECTED_CAMERAS:

    for j in range(len(uv_coords[i])):
        world_coords[i].append(CHESS_WORLD.copy().tolist())

    my_world_coords = np.expand_dims(np.array(world_coords[i]).astype(np.float32), -2)
    my_uv_coords = np.expand_dims(np.array(uv_coords[i]).astype(np.float32), -2)

    print(my_world_coords.shape)
    print(my_uv_coords.shape)

    print(f"calculating camera calibration, camera idx: {i}")
    print("imgs:")
    [print(img_path) for img_path in calibration_img_names[i]]
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
    # rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(my_world_coords, my_uv_coords, (calibration_imgs[i][0].shape[1], calibration_imgs
    
    N_OK = len(my_uv_coords)
    K = np.zeros((3, 3))
    K[0,0] = 500
    K[1,1] = 500
    K[0, 2] = 1920/2
    K[1, 2] = 1920/2  

    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

    print(K.shape)
    print(D.shape)
    print(calibration_imgs[i][0].shape[1], calibration_imgs[i][0].shape[0])
    print(len(rvecs))
    print(rvecs[0].shape)

    rms, _, _, rvecs, tvecs = \
        cv2.fisheye.calibrate(
            my_world_coords,
            my_uv_coords,
            (calibration_imgs[i][0].shape[1], calibration_imgs[i][0].shape[0]),
            K,
            D,
            rvecs,
            tvecs,
            calibration_flags,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
        )
    print("done calculating camera calibration")
    print("Found " + str(N_OK) + " valid images for calibration")
    print("\nRMS:", rms)
    print("camera matrix:\n", K)
    print("distortion coefficients: ", D.ravel())

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

            # uv_corners = transform_world_to_camera(newcameramtx, get_rot_from_euler(*rvecs[0].flatten()), tvecs[0], P_w)

            axes[0].plot(my_uv_coords[j].reshape((-1, 2))[:, 0], my_uv_coords[j].reshape((-1, 2))[:, 1], 'r+', label="original_corners")
            axes[0].set_title(f"Cam {i} w/ Intrinsics and Distortion Coefficients")
            axes[0].legend()

        img_dim = (img.shape[1], img.shape[0])

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, img_dim, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        if DO_PLOTS_UNDIST:
        # undistorted_image = undistorted_image[y:y+h, x:x+w]
            axes[1].imshow(undistorted_img[:, :, [2, 1, 0]])
            axes[1].set_title("Undistorted Image")
            plt.show()
            plt.close(fig)
