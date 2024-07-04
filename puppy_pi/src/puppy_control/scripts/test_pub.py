#!/usr/bin/env python3
# coding=utf8

import rospy
from puppy_control.msg import Pose

if __name__ == '__main__':
    rospy.init_node('pose_pub')
    pub = rospy.Publisher("/puppy_control/pose", Pose, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        msg = Pose()
        msg.roll=0
        pub.publish(msg)
        rate.sleep()
