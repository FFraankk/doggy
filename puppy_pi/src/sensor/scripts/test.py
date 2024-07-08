#!/usr/bin/python3
#coding=utf8
import os
import sys
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def setBuzzer():
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, 1)
    time.sleep(1)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, 0)

if __name__ == '__main__':
    setBuzzer()
