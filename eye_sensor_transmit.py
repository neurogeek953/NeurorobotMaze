#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 21:59:09 2018

@author: TEB
"""

@nrp.MapRobotSubscriber("camera", Topic('/husky/camera', sensor_msgs.msg.Image))
@nrp.MapSpikeSource("red_left_eye", nrp.brain.sensors_righteye[slice(0, 3, 1)], nrp.poisson)
@nrp.MapSpikeSource("red_right_eye", nrp.brain.sensors_lefteye[slice(39, 42, 1)], nrp.poisson)
@nrp.MapSpikeSource("green_blue_eye", nrp.brain.sensors_righteye[slice(4, 7, 1)], nrp.poisson)
@nrp.MapSpikeSource("green_blue_eye", nrp.brain.sensors_lefteye[slice(43, 46, 1)], nrp.poisson)
@nrp.Robot2Neuron()
def eye_sensor_transmit(t, camera, red_left_eye, red_right_eye, green_blue_eye):
    image_results = hbp_nrp_cle.tf_framework.tf_lib.detect_red(image=camera.value)
    red_left_eye.rate = 40000.0 * image_results.left
    red_right_eye.rate = 40000.0 * image_results.right
    green_blue_eye.rate = 75.0 * image_results.go_on