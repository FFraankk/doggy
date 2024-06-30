#!/usr/bin/env python3
# encoding: utf-8
import os
import time
import threading
import sqlite3 as sql
import numpy as np
import sys


from ServoCmd import setServoPulse

from PuppyInstantiate import PuppyInstantiate as puppy

# from HiwonderPuppy import HiwonderPuppy, PWMServoParams
# puppy = HiwonderPuppy(setServoPulse = setServoPulse, servoParams = PWMServoParams(), dof='8')

HomePath = '/home/pi'
# print('HomePath',HomePath)
runningAction = False
stopRunning = False
online_action_num = None
online_action_times = -1
update_ok = False
action_group_finish = True


def runActionGroup(num, wait = False):
    global runningAction
    threading.Thread(target=runAction, args=(num, )).start()
    if wait == False:return
    
    t = time.time() # 等待动作组做结束
    time.sleep(0.02)
    while time.time() - t < 30:#超时强制跳出
        time.sleep(0.001)
        if runningAction == False:
            break
        

def stopActionGroup():
    global stopRunning, online_action_num, online_action_times, update_ok
    update_ok = False
    stopRunning = True
    online_action_num = None
    online_action_times = -1
    time.sleep(0.1)

def stop_servo():
    for i in range(16):
        pass
        # stopBusServo(i+1) 

def action_finish():
    global action_group_finish
    return action_group_finish  

def runAction(actNum):
    '''
    运行动作组，无法发送stop停止信号
    :param actNum: 动作组名字 ， 字符串类型
    :param times:  运行次数
    :return:
    '''
    global runningAction
    global stopRunning
    global online_action_times
    if actNum is None:
        return
    actNum = HomePath + "/PuppyPi_PC_Software/ActionGroups/" + actNum
    stopRunning = False
    if os.path.exists(actNum) is True:
        if runningAction is False:
            runningAction = True
            ag = sql.connect(actNum)
            cu = ag.cursor()
            cu.execute("select * from ActionGroup")

            puppy.servo_force_run()
            time.sleep(0.01)
            while True:
                act = cu.fetchone()
                if stopRunning is True:
                    stopRunning = False                   
                    break
                if act is not None:
                    if type(act[2]) is int:
                        for i in range(0, len(act)-2, 1):
                            setServoPulse(i+1, act[2 + i], act[1])
                                
                    elif type(act[2]) is float:
                        rotated_foot_locations = np.zeros(12)
                        for i in range(0, len(act)-2):
                            value = act[i+2]
                            rotated_foot_locations[i] = float(value)
                        rotated_foot_locations = rotated_foot_locations.reshape(4,3)
                        rotated_foot_locations = rotated_foot_locations.T
                        rotated_foot_locations = rotated_foot_locations/100
                        joint_angles = puppy.fourLegsRelativeCoordControl(rotated_foot_locations)
                        
                        puppy.sendServoAngle(joint_angles, act[1])#, force_execute = True
                        # joint_angles = puppy.four_legs_inverse_kinematics_relative_coord(rotated_foot_locations, puppy.config)
                        # puppy.send_servo_commands(PWMServoParams(), joint_angles, act[1])
                        

                    time.sleep(float(act[1])/1000.0)
                else:   # 运行完才退出
                    break

            runningAction = False
            cu.close()
            ag.close()
    else:
        runningAction = False
        print("未能找到动作组文件")

def online_thread_run_acting():
    global online_action_times, online_action_num, update_ok, action_group_finish
    while True:
        if update_ok:
            if online_action_times == 0:
                # 无限次运行
                if action_group_finish:
                    action_group_finish = False
                runAction(online_action_num)                
            elif online_action_times > 0:
                # 有次数运行
                if action_group_finish:
                    action_group_finish = False
                runAction(online_action_num)
                online_action_times -= 1    # 运行完成后，进入空载                
                if online_action_times == 0:
                    online_action_times = -1
            else:
                # 空载
                if not action_group_finish:
                    action_group_finish = True
                time.sleep(0.001)
        else:
            if not action_group_finish:
                action_group_finish = True
            time.sleep(0.001)
            
def start_action_thread():
    th1 = threading.Thread(target=online_thread_run_acting)
    th1.setDaemon(True)  # 设置为后台线程，这里默认是True
    th1.start()
    
def change_action_value(actNum, actTimes):
    global online_action_times, online_action_num, update_ok, stopRunning, action_group_finish
    
    if action_group_finish:
        online_action_times = actTimes
        online_action_num = actNum
        stopRunning = False
        update_ok = True
