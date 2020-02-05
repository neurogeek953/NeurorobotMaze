#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 21:46:26 2018

@author: TEB
"""

@nrp.NeuronMonitor(nrp.brain.record[slice(0, 46, 1)], nrp.spike_recorder)
def all_neurons_spike_monitor(t):
    return True