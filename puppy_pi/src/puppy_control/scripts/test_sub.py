#!/usr/bin/python3
# coding=utf8

import rospy
from puppy_control.msg import Pose

def pose_callback(Pose):
    rospy.loginfo(Pose.roll)

if __name__ == '__main__':
    rospy.init_node('pose_listener')
    sub = rospy.Subscriber("/puppy_control/pose", Pose, pose_callback,queue_size=10)
    rospy.spin()