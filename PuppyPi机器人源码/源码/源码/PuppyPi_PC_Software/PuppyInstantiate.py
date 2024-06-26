#!/usr/bin/env python3
# encoding: utf-8

from ServoCmd import setServoPulse

from HiwonderPuppy import HiwonderPuppy, PWMServoParams

PuppyInstantiate = HiwonderPuppy(setServoPulse = setServoPulse, servoParams = PWMServoParams(), dof='8')