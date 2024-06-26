#!/usr/bin/python3
# coding=utf8
import os, sys, math
import numpy as np
# import cv2
import threading
import pygame

# sys.path.append('/home/pi/PuppyPi_PC_Software/')
from ServoCmd import *
# from mpu6050 import MPU6050
from HiwonderPuppy import HiwonderPuppy, PWMServoParams

puppy = HiwonderPuppy(setServoPulse = setServoPulse, servoParams = PWMServoParams(), dof = '8')

key_map = {"PSB_CROSS":2, "PSB_CIRCLE":1, "PSB_SQUARE":3, "PSB_TRIANGLE":0,
    "PSB_L1": 4, "PSB_R1":5, "PSB_L2":6, "PSB_R2":7,
    "PSB_SELECT":8, "PSB_START":9, "PSB_L3":10, "PSB_R3":11};
action_map = ["CROSS", "CIRCLE", "", "SQUARE", "TRIANGLE", "L1", "R1", "L2", "R2", "SELECT", "START", "", "L3", "R3"]

Stand = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
# Stand = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':0, 'stance_x':0, 'stance_y':0}
# Stand = {'roll':math.radians(0), 'pitch':math.radians(-20), 'yaw':0.000, 'height':-9, 'x_shift':-0.1, 'stance_x':0, 'stance_y':0}
Bend = {'roll':math.radians(0), 'pitch':math.radians(-14), 'yaw':0.000, 'height':-9, 'x_shift':-0.1, 'stance_x':0, 'stance_y':0}
PuppyPoseDefault = {'stance_x':0, 'stance_y':0, 'x_shift':-0.5, 'height':-10, 'pitch':-0.000}
PuppyPose = Bend.copy()
# PuppyPose = {'roll':math.radians(0), 'pitch':math.radians(5), 'yaw':0.000, 'height':-10, 'x_shift':-1.48, 'stance_x':0, 'stance_y':0}

GaitConfigFast = {'overlap_time':0.15, 'swing_time':0.1, 'clearance_time':0.0, 'z_clearance':4}
# GaitConfigSlow = {'overlap_time':0.0, 'swing_time':0.8, 'clearance_time':0.8, 'z_clearance':4}
GaitConfig = GaitConfigFast.copy()
GaitConfig = {'overlap_time':0.1, 'swing_time':0.15, 'clearance_time':0.0, 'z_clearance':3}

PuppyMove = {'x':0, 'y':0, 'yaw_rate':0}


def joystick_init():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        js=pygame.joystick.Joystick(0)
        js.init()
        jsName = js.get_name()
        print("Name of the joystick:", jsName)
        jsAxes=js.get_numaxes()
        print("Number of axif:",jsAxes)
        jsButtons=js.get_numbuttons()
        print("Number of buttons:", jsButtons)
        jsBall=js.get_numballs()
        print("Numbe of balls:", jsBall)
        jsHat= js.get_numhats()
        print("Number of hats:", jsHat)

# mpu = MPU6050()
# puppy.imu = mpu
def stance(x = 0, y = 0, z = -15, x_shift = 0):# 单位cm
    # x_shift越小，走路越前倾，越大越后仰,通过调节x_shift可以调节小狗走路的平衡
    return np.array([
                        [x + x_shift, x + x_shift, -x + x_shift, -x + x_shift],
                        [y, y, y, y],
                        [z, z, z, z],
                    ])#此array的组合方式不要去改变


puppy.stance_config(stance(PuppyPose['stance_x'],PuppyPose['stance_y'],PuppyPose['height'],PuppyPose['x_shift']), PuppyPose['pitch'], roll = 0)# 标准站姿
# puppy.gait_config(overlap_time = 0.1, swing_time = 0.15, z_clearance = 3)
puppy.gait_config(overlap_time = GaitConfig['overlap_time'], swing_time = GaitConfig['swing_time']
                                , clearance_time = GaitConfig['clearance_time'], z_clearance = GaitConfig['z_clearance'])
# overlap_time:4脚全部着地的时间，swing_time：2脚离地时间，z_clearance：走路时，脚抬高的距离

puppy.start() # 启动
puppy.move_stop()
# time.sleep(1)


# puppy.get_coord()
# time.sleep(1.00)
# puppy.move(x=0, y=0, yaw_rate = 0)
# # # puppy.move(x=10, y=0, yaw_rate = 0)#18/57.3
# # # puppy.stance_config(stance(0,0,-13,0), pitch = 0, roll = 0)
# time.sleep(10)
# puppy.move_stop()
# time.sleep(0.2)

# tt = 1

# puppy.move(x=6, y=0, yaw_rate = 0.0)#18/57.3
# while True:
#     time.sleep(0.0001)
#     pass

connected = False
lastTime = time.time()
try:
    while True:
        pass

        if os.path.exists("/dev/input/js0") is True:
            if connected is False:
                joystick_init()
                jscount =  pygame.joystick.get_count()
                if jscount > 0:
                    try:
                        js=pygame.joystick.Joystick(0)
                        js.init()
                        connected = True
                    except Exception as e:
                        print(e)
                else:
                    pygame.joystick.quit()
        else:
            if connected is True:
                connected = False
                js.quit()
                pygame.joystick.quit()
        if connected is True:
            pygame.event.pump()     
            actName = None
            times = 1
            try:
                # buttons = [js.get_button(i) for i in range(13)]
                # print(buttons)
                if js.get_button(key_map["PSB_R1"]):
                    actName = 'right_kick'
                    if PuppyPose['x_shift'] > -6:PuppyPose['x_shift'] -= 0.03
                if js.get_button(key_map["PSB_R2"]):
                    actName = 'turn_right'
                    if PuppyPose['x_shift'] < 6:PuppyPose['x_shift'] += 0.03
                    

                if js.get_button(key_map["PSB_L1"]):
                    actName = 'left_kick'
                    if PuppyPose['pitch'] < 30/57.3:PuppyPose['pitch'] += 0.003
                elif js.get_button(key_map["PSB_L2"]):
                    actName = 'turn_left'
                    if PuppyPose['pitch'] > -30/57.3:PuppyPose['pitch'] -= 0.003
                    

                if js.get_button(key_map["PSB_SQUARE"]): #正方形
                    actName = 'left_shot_fast'
                    PuppyMove['y']  = 15 #15
                elif js.get_button(key_map["PSB_CIRCLE"]): #圈
                    actName = 'right_shot_fast'
                    PuppyMove['y'] = -15
                else:
                    PuppyMove['y'] = 0
                if js.get_button(key_map["PSB_TRIANGLE"]): #三角
                    actName = 'wave'
                    PuppyPose['height'] -= 0.03
                    if PuppyPose['height'] < -16:PuppyPose['height'] = -16
                elif js.get_button(key_map["PSB_CROSS"]): #叉
                    actName = 'bow'
                    PuppyPose['height'] += 0.03
                    if PuppyPose['height'] > -5:PuppyPose['height'] = -5

                lx = js.get_axis(0)
                ly = js.get_axis(1)
                # print('lx: ',lx, 'ly: ',ly)
                if lx < -0.9 :
                    actName = 'left_move_fast'
                    PuppyMove['yaw_rate'] = 10/57.3 #40/57.3
                elif lx > 0.9:             
                    actName = 'right_move_fast'
                    PuppyMove['yaw_rate'] = -10/57.3
                else:
                    PuppyMove['yaw_rate'] = 0

                if ly < -0.9 :
                    actName = '-ly'
                    PuppyMove['x'] = 3 #23
                elif ly > 0.9:             
                    actName = 'ly'
                    PuppyMove['x'] = -15
                else:
                    PuppyMove['x'] = 0
                # l3_state = js.get_button(key_map["PSB_L3"])
                # if ly < -0.9 :
                #     if not l3_state:
                #         last_status = 'go'
                #         actName = 'go_forward'
                #         times = 0
                # elif ly > 0.9:
                #     if not l3_state:
                #         last_status = 'back'
                #         actName = 'back_fast'
                #         times = 0
                # else:
                #     if (last_status == 'go' or last_status == 'back') and actName is None:
                #         print('stopActionGroup')
                #         # AGC.stopActionGroup()
                #         last_status = ''
                if js.get_button(key_map["PSB_START"]):
                    actName = 'stand_slow'
                    PuppyPose = PuppyPoseDefault.copy()
                    PuppyMove = {'x':0, 'y':0, 'yaw_rate':0}
                    print('PSB_START')

                puppy.stance_config(stance(PuppyPose['stance_x'],PuppyPose['stance_y'],PuppyPose['height'],PuppyPose['x_shift']), PuppyPose['pitch'], roll = 0)
                if list(PuppyMove.values()) == [0,0,0]:
                    puppy.move(0, 0, 0)
                    puppy.move_stop()
                else:
                    puppy.move(PuppyMove['x'], PuppyMove['y'], PuppyMove['yaw_rate'])
                    print(PuppyMove)
                if time.time() - lastTime > 1:
                    lastTime = time.time()
                    # print('height=%f,x_shift=%f,pitch=%f'%(PuppyPose['height'],PuppyPose['x_shift'],PuppyPose['pitch']*57.29))
                    # print('puppy.coord:')
                    # print(puppy.get_coord())

            except Exception as e:
                print(e)
                connected = False

        time.sleep(0.01)

except KeyboardInterrupt:
    puppy.move_stop()
    time.sleep(0.2)
    pass
