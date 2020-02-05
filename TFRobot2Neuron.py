#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 19:01:35 2018

@author: TEB
"""

"""Transfer Function monitoring the robot's position"""
@nrp.MapCSVRecorder("recorder", filename="robot_position.csv", headers=["x", "y", "z"])
@nrp.MapRobotSubscriber("position", Topic('/gazebo/model_states', gazebo_msgs.msg.ModelStates))
@nrp.MapVariable("robot_index", global_key="robot_index", initial_value=None)
@nrp.Robot2Neuron()
def csv_robot_position(t, position, recorder, robot_index):
    if not isinstance(position.value, type(None)):
        # determine if previously set robot index has changed
        if robot_index.value is not None:
            # if the value is invalid, reset the index below
            if robot_index.value >= len(position.value.name) or\
               position.value.name[robot_index.value] != 'robot':
                robot_index.value = None
        # robot index is invalid, find and set it
        if robot_index.value is None:
            # 'robot' is guaranteed by the NRP, if not found raise error
            robot_index.value = position.value.name.index('robot')
        # record the current robot position
        recorder.record_entry(position.value.pose[robot_index.value].position.x,
                              position.value.pose[robot_index.value].position.y,
                              position.value.pose[robot_index.value].position.z)
        

"Transfer Function Monitoring joints"
@nrp.MapRobotSubscriber("joint_state", Topic('/joint_states', sensor_msgs.msg.JointState))
@nrp.MapCSVRecorder("recorder", filename="all_joints_positions.csv", headers=["Name", "time", "Position"])
@nrp.Robot2Neuron()
def csv_joint_state_monitor(t, joint_state, recorder):
    if not isinstance(joint_state.value, type(None)):
        for i in range(0, len(joint_state.value.name)):
            recorder.record_entry(joint_state.value.name[i], t, joint_state.value.position[i])

"""Transfer Function from Camera to Neuron"""
@nrp.MapRobotSubscriber("camera", Topic('/husky/camera', sensor_msgs.msg.Image))
@nrp.MapSpikeSource("red_left_eye", nrp.brain.sensors[slice(0, 2, 3, 41, 43, 44)], nrp.poisson)
@nrp.MapSpikeSource("green_blue_eye", nrp.brain.sensors[slice(1, 4, 5, 6, 7, 42, 45, 46, 47,48)], nrp.poisson)
@nrp.Robot2Neuron()
def eye_sensor_transmit(t, camera, red_left_eye, red_right_eye, green_blue_eye):
    image_results = hbp_nrp_cle.tf_framework.tf_lib.detect_red(image=camera.value)
    red_left_eye.rate = 40000.0 * image_results.left
    red_right_eye.rate = 40000.0 * image_results.right
    green_blue_eye.rate = 75.0 * image_results.go_on





