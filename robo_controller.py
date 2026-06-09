"""
This is a script that facilitates tele-operation of a robot to record data to use for imitation learning.

It uses matplotlib to display a UI of what the robot sees from cameras, in addition to its projected path via current command velocity, its pitch and roll visualized with horizon lines, and other data. It displays current cmd vel, and 
on keypress can adjust this. It also displays current text instruction and on press of a button can toggle to the next one...
"""
import math
import time
from typing import Tuple
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt

INSTRUCTIONS = ("Move forward across the bridge and turn left on the path after the bridge. Continue until you reach the large concrete building on the right, Marshgate.", "From here, continue forward past the large concrete building, Marshgate, and continue on as you pass trees and the river on the left.", "The concrete blocks should be directly ahead.")

VEL_X = (-0.5, -0.25, 0.0, 0.25, 0.5)
VEL_Y = (-0.5, -0.25, 0.0, 0.25, 0.5)
VEL_THETA = (-math.pi/2, -math.pi/4, 0.0, math.pi/4, math.pi/2)
N_CAM = 2
IMG_SHAPE = (3840, 1920, 3)



class RoboTeleop:
    def __init__(self, instructions: Tuple[str], vel_x_options: Tuple[float], vel_y_options: Tuple[float],          vel_theta_options: Tuple[float], n_cam: int, img_shape = (3840, 1920, 3)):
        self.n_instructions = len(instructions)
        self.instructions = instructions

        self.exit_flag = False

        assert vel_x_options[len(vel_x_options)//2] == 0.0
        assert vel_y_options[len(vel_y_options)//2] == 0.0
        assert vel_theta_options[len(vel_theta_options)//2] == 0.0

        self.not_moving = True
        self.n_vel_x = len(vel_x_options)
        self.cur_x_sel = self.n_vel_x // 2
        self.vel_x_options = vel_x_options
        self.n_vel_y = len(vel_y_options)
        self.cur_y_sel = self.n_vel_y // 2
        self.vel_y_options = vel_y_options
        self.n_vel_theta = len(vel_theta_options)
        self.cur_vtheta_sel = self.n_vel_theta // 2
        self.vel_theta_options = vel_theta_options

        self.n_cam = n_cam
        self.cur_imgs = np.zeros((n_cam, *img_shape), dtype=np.uint8)
        self.img_shape = img_shape

        self.zero_vel_cmd = (0.0, 0.0, 0.0)
        self.cur_vel_cmd = (0.0, 0.0, 0.0)
        plt.ion()
        self.fig, self.axes = plt.subplots(1, n_cam + 1, figsize=(14, 10))
        self.fig.tight_layout()

        self.axes[-1].get_xaxis().set_visible(False)
        self.axes[-1].get_yaxis().set_visible(False)

        self.fontsize = 12
        self.font_x_inc = 15
        self.font_y_inc = 10
        self.float_round = 2

        self.axes_text_lim = 100
        self.axes[-1].set_xlim(0.0, self.axes_text_lim)
        self.axes[-1].set_ylim(0.0, self.axes_text_lim)

        self.vel_objs = []
        self.x_vel_obj_idx = 0
        self.y_vel_obj_idx = 1
        self.vtheta_obj_idx = 2
        
        cur_vel_obj = 0
        for vel_sel, n_vel, vel_options, text_prefix in ((self.cur_x_sel, self.n_vel_x, self.vel_x_options, "vx: "),
                                            (self.cur_y_sel, self.n_vel_y, self.vel_y_options, "vy: "),
                                            (self.cur_vtheta_sel, self.n_vel_theta, self.vel_theta_options, "vt: ")):
            self.vel_objs.append([])
            for i in range(n_vel):
                color = "green" if i != vel_sel else "red"
                prefix_to_add = "" if i != 0 else text_prefix
                text_suffix = ", " if i != n_vel - 1 else ""
                vel_str = str(round(vel_options[i], self.float_round ))
                prefix_dist_incr = len(text_prefix) if i != 0 else 0
                print(vel_str)
                text_obj = self.axes[-1].text(i * self.axes_text_lim // n_vel, cur_vel_obj * self.axes_text_lim // n_vel, prefix_to_add + vel_str + text_suffix, fontsize=self.fontsize, color=color)

                self.vel_objs[cur_vel_obj].append(text_obj)
            cur_vel_obj += 1

        # set_text

    def init_keypress(self, fn_ptr):
        self.fig.canvas.mpl_connect('key_press_event', fn_ptr)

    def handle_keypress(self, event):
        update_vel_obj = False
        counter_diff = 1
        cur_idx = None
        vel_options = None

        key_x_incr = "i"
        key_x_decr = "k"

        key_y_incr = "j"
        key_y_decr = "l"

        key_theta_incr = "u"
        key_theta_decr = "o"

        if event.key == key_x_incr:
            vel_obj_idx = self.x_vel_obj_idx
            update_vel_obj = True
            cur_idx = self.cur_x_sel
            vel_options = self.vel_x_options
        elif event.key == key_x_decr:
            vel_obj_idx = self.x_vel_obj_idx
            counter_diff = -1
            update_vel_obj = True
            cur_idx = self.cur_x_sel
            vel_options = self.vel_x_options
        elif event.key == key_y_incr:
            vel_obj_idx = self.y_vel_obj_idx
            update_vel_obj = True
            cur_idx = self.cur_y_sel
            vel_options = self.vel_y_options
        elif event.key == key_y_decr:
            vel_obj_idx = self.y_vel_obj_idx
            counter_diff = -1
            update_vel_obj = True
            cur_idx = self.cur_y_sel
            vel_options = self.vel_y_options
        elif event.key == key_theta_incr:
            vel_obj_idx = self.vtheta_obj_idx
            update_vel_obj = True
            cur_idx = self.cur_vtheta_sel
            vel_options = self.vel_theta_options
        elif event.key == key_theta_decr:
            vel_obj_idx = self.vtheta_obj_idx
            counter_diff = -1
            update_vel_obj = True
            cur_idx = self.cur_vtheta_sel
            vel_options = self.vel_theta_options



    
        if update_vel_obj:
            cur_idx += counter_diff
            if cur_idx == -1 or cur_idx == len(vel_options):
                pass
            else:
                # update color of prior counter, update color of current counter
                self.vel_objs[vel_obj_idx][cur_idx].set_c("red")
                self.vel_objs[vel_obj_idx][cur_idx + counter_diff * -1].set_c("green")
                
                if event.key == key_x_incr:
                    self.cur_x_sel = cur_idx
                elif event.key == key_x_decr:
                    self.cur_x_sel = cur_idx
                elif event.key == key_y_incr:
                    self.cur_y_sel = cur_idx
                elif event.key == key_y_decr:
                    self.cur_y_sel = cur_idx
                elif event.key == key_theta_incr:
                    self.cur_vtheta_sel = cur_idx
                elif event.key == key_theta_decr:
                    self.cur_vtheta_sel = cur_idx


        if event.key == "q":
            self.exit_flag = True

    def tick(self):
        self.fig.canvas.draw_idle()
        plt.pause(0.001)
        return self.exit_flag


        

if __name__ == "__main__":
    robo_tele = RoboTeleop(INSTRUCTIONS, VEL_X, VEL_Y, VEL_THETA, N_CAM, IMG_SHAPE)


    def on_press(event):
        print('press', event.key)
        robo_tele.handle_keypress(event)
        sys.stdout.flush()



    robo_tele.init_keypress(on_press)
    start_time = time.time()

    while time.time() - start_time < 5.0:
        ret = robo_tele.tick()
        if ret:
            break
        time.sleep(0.01)
