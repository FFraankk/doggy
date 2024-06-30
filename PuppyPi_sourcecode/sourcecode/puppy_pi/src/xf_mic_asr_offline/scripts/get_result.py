#!/usr/bin/env python3
# coding=utf8
import json
import rospy
from std_msgs.msg import String, Int32
from puppy_control.srv import SetRunActionName


do = ['来','来个','做个','表演','表演个','表演一个']
# action = []

def words_callback(msg):
    words = json.dumps(msg.data, ensure_ascii=False)[1:-1]
    print('words:', words)

    if any([k in words for k in ("立正" , "站好" , "站立")]):
        runActionGroup_srv('stand.d6ac',True)
    elif "双腿站立" in words:
        runActionGroup_srv('2_legs_stand.d6ac',True)
    elif ("坐下") in words:
        runActionGroup_srv('sit.d6ac',True)
    elif ("趴下") in words:
        runActionGroup_srv('lie_down.d6ac',True)
    elif any([k in words for k in ("握手" , "握个手")]):
        runActionGroup_srv('shake_hands.d6ac',True)
    elif ("作揖") in words:
        runActionGroup_srv('bow.d6ac',True)
    elif any([k in words for k in ("点头" ,"点个头")]):
        runActionGroup_srv('nod.d6ac',True)
    elif ("摇头") in words:
        runActionGroup_srv('shake_head.d6ac',True)
    elif ("拳击") in words:
        runActionGroup_srv('boxing.d6ac',True)
    elif ("伸懒腰") in words:
        runActionGroup_srv('stretch.d6ac',True)
    elif any([k in words for k in ("撒尿","嘘嘘")]):
        runActionGroup_srv('pee.d6ac',True)
    elif ("俯卧撑") in words:
        runActionGroup_srv('push-up.d6ac',True)
    elif any([k in words for k in ("太空漫步" ,"太空步")]):
        runActionGroup_srv('spacewalk.d6ac',True)

def angle_callback(msg):
    angle = msg.data
    print('angle:', angle)

if __name__ == "__main__":
    rospy.init_node('xf_mic', anonymous=True)
    rospy.Subscriber('/voice_words', String, words_callback)
    rospy.Subscriber('/mic/awake/angle', Int32, angle_callback)
    runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)

    try:
        rospy.spin()
    except Exception as e:
        rospy.logerr(str(e))
