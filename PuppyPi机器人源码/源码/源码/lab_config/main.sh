#!/bin/bash
source /opt/ros/noetic/setup.bash
source /home/pi/puppy_pi/devel/setup.bash
# export ROS_HOSTNAME=192.168.149.1
# export ROS_MASTER_URI=http://192.168.149.1:11311

python3 /home/pi/lab_config/main.py
