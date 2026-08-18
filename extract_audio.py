import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import rosbag2_py

import PIL

import cv2
import os
import numpy as np

from rclpy.serialization import deserialize_message


from sensor_msgs.msg import Image, CompressedImage, Imu
from std_msgs.msg import UInt8MultiArray 
from cv_bridge import CvBridge

from rclpy.parameter import Parameter

BAG_FILE = "/home/developer/ros_ws/rosbags/rosbag2_2026_08_18-09_34_05-audio-ex"
OUT_DIR = "/home/developer/ros_ws/rosbags"

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


    def extract_audio(self):
        
        all_audio_data = bytearray()

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
            if topic == "/dual_fisheye/audio_aac":
                msg_type = UInt8MultiArray
            else:
                continue

            msg = deserialize_message(data, msg_type)

            if topic == "/dual_fisheye/audio_aac":
                timestamp_big_endian = msg.data[:8]
                timestamp = int.from_bytes(timestamp_big_endian, byteorder='big', signed=True)
                audio_data = msg.data[8:]
                all_audio_data.extend(audio_data)
        return all_audio_data
            

def main(args=None):
    try:
        rclpy.init(args=args)
        sbr = SimpleBagReader()
        all_audio = sbr.extract_audio()
        # ffmpeg -i audio_experiment.aac -acodec libmp3lame audio.mp3 to mp3
        out_path = os.path.join(OUT_DIR, "audio_experiment.aac")
        with open(out_path, "wb") as file:
            file.write(all_audio)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
