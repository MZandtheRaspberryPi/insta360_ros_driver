import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import rosbag2_py

import PIL

import cv2
import os
import numpy as np

from rclpy.serialization import deserialize_message

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt

from sensor_msgs.msg import Image, CompressedImage, Imu
from cv_bridge import CvBridge

from rclpy.parameter import Parameter

BAG_FILE = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali-chess-4-uncompr-rosbag2_2026_05_26-15_19_39"
OUT_DIR = "/home/developer/ros_ws/src/hardware/insta360_ros_driver/cali_imgs_chess_4"

class SimpleBagReader(Node):

    def __init__(self):
        super().__init__("simple_bag_reader")

        # self.get_parameter('use_sim_time').value = True
        # self.declare_parameter('use_sim_time', True)

        # param_bl = Parameter('use_sim_time', Parameter.Type.BOOL, True)
        # self.set_parameters([param_bl])

        self.reader = rosbag2_py.SequentialReader()
        storage_options = rosbag2_py.StorageOptions(uri=BAG_FILE, storage_id="sqlite3")
        converter_options = rosbag2_py.ConverterOptions("", "")
        self.reader.open(storage_options, converter_options)
        self.br = CvBridge()


    def make_plots(self):
        
        first_timestamp = None

        i = 0
        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()

            timestamp_sec = timestamp / 1e9

            if first_timestamp is None:
                first_timestamp = timestamp_sec
                timestamp_sec_from_start = 0.0
            else:
                timestamp_sec_from_start = timestamp_sec - first_timestamp

            msg_type = None
            if topic == "/dual_fisheye/image/compressed":
                msg_type = CompressedImage
            elif topic == "/dual_fisheye/image":
                msg_type = Image
            elif topic == "/imu/data_raw":
                msg_type = Imu
            else:
                continue

            msg = deserialize_message(data, msg_type)

            if topic == "/dual_fisheye/image/compressed":
                color_img_cv = self.br.compressed_imgmsg_to_cv2(msg, "rgb8")
             
                im_pil = PIL.Image.fromarray(color_img_cv)
                im_pil.save(os.path.join(OUT_DIR, f"img_raw_{str(i).zfill(7)}_{timestamp_sec_from_start}.png"))
                i += 1
            
            if topic == "/dual_fisheye/image":
                color_img_cv = self.br.imgmsg_to_cv2(msg, "rgb8")
                im_pil = PIL.Image.fromarray(color_img_cv)
                im_pil.save(os.path.join(OUT_DIR, f"img_raw_{str(i).zfill(7)}_{timestamp_sec_from_start}.png"))
                i += 1

            # raise ValueError
            

def main(args=None):
    try:
        rclpy.init(args=args)
        sbr = SimpleBagReader()
        sbr.make_plots()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
