#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 19:01:01 2018

@author: TEB
"""

"Transfer Function Monitoring Front Left Propeller"
@nrp.NeuronMonitor(nrp.brain.actors[25], nrp.population_rate)
def frontleft_propeller_neuron_rate_monitor(t):
    return True

"Transfer Function Monitoring Front Right Propeller"
@nrp.NeuronMonitor(nrp.brain.actors[26], nrp.population_rate)
def frontright_propeller_neuron_rate_monitor(t):
    return True

"Transfer Function Monitoring Back Left Propeller"
@nrp.NeuronMonitor(nrp.brain.actors[27], nrp.population_rate)
def frontright_propeller_neuron_rate_monitor(t):
    return True

"Transfer Function Monitoring Back Right Propeller"
@nrp.NeuronMonitor(nrp.brain.actors[28], nrp.population_rate)
def frontright_propeller_neuron_rate_monitor(t):
    return True

"""Transfer Function Actuating the Drones Four Propellers"""
@nrp.MapSpikeSink("left_wheel_neuron", nrp.brain.actors[25], nrp.leaky_integrator_alpha)
@nrp.MapSpikeSink("right_wheel_neuron", nrp.brain.actors[26], nrp.leaky_integrator_alpha)
@nrp.MapSpikeSink("left_wheel_neuron", nrp.brain.actors[27], nrp.leaky_integrator_alpha)
@nrp.MapSpikeSink("right_wheel_neuron", nrp.brain.actors[28], nrp.leaky_integrator_alpha)
@nrp.Neuron2Robot(Topic('/husky/cmd_vel', geometry_msgs.msg.Twist))
def linear_twist(t, left_wheel_neuron, right_wheel_neuron):
    return geometry_msgs.msg.Twist(linear=geometry_msgs.msg.Vector3(x=20.0 * min(left_wheel_neuron.voltage,
                                                                                 right_wheel_neuron.voltage),
    y=0.0,
    z=0.0),
    angular=geometry_msgs.msg.Vector3(x=0.0,
                                      y=0.0,
                                      z=100.0 * (right_wheel_neuron.voltage - left_wheel_neuron.voltage)))


"""Transfer Function Recording the output of all Neurons"""
@nrp.MapCSVRecorder("recorder", filename="all_spikes.csv", headers=["id", "time"])
@nrp.MapSpikeSink("record_neurons", nrp.brain.record, nrp.spike_recorder)
@nrp.Neuron2Robot(Topic('/monitor/spike_recorder', cle_ros_msgs.msg.SpikeEvent))
def csv_spike_monitor(t, recorder, record_neurons):
    for i in range(0, len(record_neurons.times)):
        recorder.record_entry(
            record_neurons.times[i][0],
            record_neurons.times[i][1]
        )





