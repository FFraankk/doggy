import sys
import threading
from PWMServoControl import *
# import ActionGroupControl as AGC

servo = PWMServo()

servo.setThreshold(2,650,2300)
servo.setThreshold(6,650,2300)

servo.setThreshold(4,700,2350)
servo.setThreshold(8,700,2350)


def getServoPulse(id):
    return 0#getBusServoPulse(id)

def getServoDeviation(id):
    return servo.getDeviation(id)

def setServoPulse(id, pulse, use_time):
    servo.setPulse(id, pulse, use_time)

def setServoDeviation(id ,dev):
    servo.setDeviation(id, dev)
    
def saveServoDeviation(id):
    servo.saveDeviation(id)

def unloadServo(id):
    servo.unload(id)

def updatePulse(id):
    servo.updatePulse(id)
# def runActionGroup(num):
#     threading.Thread(target=AGC.runAction, args=(num, )).start()    

# def stopActionGroup():    
#     AGC.stop_action_group()  
