#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:30:50 2018

@author: TEB
"""

# -*- coding: utf-8 -*-
"""
This File contains my Virtual Brain Controller based on the architecture of the fruit fly brain.
"""
# pragma: no cover
__author__ = 'Teddy Edmond Benkohen'

from hbp_nrp_cle.brainsim import simulator as sim
#import nest as sim
import numpy as np
import logging
from pyNN.nest import PopulationView as PV
from pyNN.random import RandomDistribution
logger = logging.getLogger(__name__)


def create_brain():
    """
    Initializes PyNN with the neuronal network that has to be simulated
    :returns: The population object
    """
    ##
    ## Set up neurons
    ##
    INPUT_PARAMS = {'a': 4.0,
                    'b': 0.0000805,
                    'delta_T': 2.0,
                    'tau_w': 144.0,
                    'v_spike': 0.0,
                    'cm': .281, # ev. /1000
                    'v_rest': -70.6,
                    'tau_m': 9.3666667,
                    'e_rev_E': 0.0,
                    'e_rev_I': -80.0,
                    'v_reset': -70.6,
                    'v_thresh': -50.4,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 5.,
                    'tau_syn_I': 5.}
    
    SENSORPARAMS = {'b': 0.0,
                    'tau_w': 10.0,
                    'v_spike': 0.0,
                    'cm': 0.025,
                    'v_rest': -60.5,
                    'tau_m': 10.,
                    'e_rev_E': 0.0,
                    'e_rev_I': -75.0,
                    'v_reset': -60.5,
                    'v_thresh': -60.0,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 2.5,
                    'tau_syn_I': 7.5}
    
    GO_ON_PARAMS = {'cm': .025,
                    'v_rest': -60.5,
                    'tau_m': 10.,
                    'e_rev_E': 0.0,
                    'e_rev_I': -75.0,
                    'v_reset': -61.6,
                    'v_thresh': -60.51,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 2.5,
                    'tau_syn_I': 7.5}
    
    
    INTERMEDIATE_PARAMS = {'a': 4.0,
                           'b': 0.0000805,
                           'delta_T': 2.0,
                           'tau_w': 144.0,
                           'v_spike': 0.0,
                           'cm': .281, # ev. /1000
                           'v_rest': -70.6,
                           'tau_m': 112.4,
                           'e_rev_E': 0.0,
                           'e_rev_I': -80.0,
                           'v_reset': -70.6,
                           'v_thresh': -50.4,
                           'tau_refrac': 10.0,
                           'tau_syn_E': 5.,
                           'tau_syn_I': 5.}

    population = sim.Population(47, sim.EIF_cond_alpha_isfa_ista())
    population[:47].set(**INPUT_PARAMS)
    population[0:19].set(**SENSORPARAMS)
    population[20:24].set(**INTERMEDIATE_PARAMS)
    population[25:26].set(**GO_ON_PARAMS)
    population[27:46].set(**SENSORPARAMS)
    
    # Initialise a CIRCUIT
    CIRCUIT = population

    
    
    ##
    ## Set up synapse types
    ##

    # Synaptic Delays
    static_syn_delay = 0.1
    facil_syn_delay = 0.2
    depress_syn_delay = 0.5
    action_syn_delay = 0.0001
    
    # Synaptic tau_rec
    facil_syn_tau_rec =  RandomDistribution('normal', [100.0, 10.0])
    depress_syn_tau_rec = 800.0
    action_syn_tau_rec = 1.0
    
    # Synaptic tau_facil
    facil_syn_tau_facil = 1.0
    depress_syn_tau_facil = 0.0
    action_syn_tau_facil = 1.0
    
    #  Us
    facil_syn_U = 0.04
    depress_syn_U = 0.5
    action_syn_U = 1.0
    
    
    
    # Synaptic weights
    
    weight_retinalphotoreceptor_to_lamina = 5.0
    weight_lamina_to_lamina = 5.0
    weight_lamina_to_medula = 5.0
    weight_medula_to_medula = 8.75e-5
    weight_medula_to_lobula = 1000
    weight_lobula_to_lobula = 1.4e-4
    weight_lobula_to_cortex = 1.0
    weight_cortex_to_cortex = 1.5e-2
    weight_cortex_to_lobula = 5.0
    weight_cortex_to_actors = 1000
    
    # Set Synapse types
    
    synapse_retinalphotoreceptor_to_lamina = sim.StaticSynapse(delay = static_syn_delay, weight = weight_retinalphotoreceptor_to_lamina)
    synapse_lamina_to_lamina = sim.StaticSynapse(delay = static_syn_delay, weight = weight_lamina_to_lamina)
    synapse_lamina_to_medula = sim.StaticSynapse(delay = static_syn_delay, weight = weight_lamina_to_medula)
    synapse_medula_to_medula = sim.StaticSynapse(delay = static_syn_delay, weight = weight_medula_to_medula)
    synapse_medula_to_lobula = sim.StaticSynapse(delay = static_syn_delay, weight = weight_medula_to_lobula)
    synapse_lobula_to_lobula = sim.StaticSynapse(delay = static_syn_delay, weight = weight_lobula_to_lobula)
    synapse_lobula_to_cortex = sim.StaticSynapse(delay = static_syn_delay, weight = weight_lobula_to_cortex)
    synapse_cortex_to_lobula = sim.TsodyksMarkramSynapse(tau_facil = depress_syn_tau_facil,
                                                         delay = depress_syn_delay,
                                                         weight = weight_cortex_to_lobula,
                                                         U = depress_syn_U,
                                                         tau_rec = depress_syn_tau_rec)
    synapse_cortex_to_cortex = sim.TsodyksMarkramSynapse(tau_facil = facil_syn_tau_facil,
                                                         delay = facil_syn_delay,
                                                         weight = weight_cortex_to_cortex,
                                                         U = facil_syn_U,
                                                         tau_rec = facil_syn_tau_rec)
    synapse_cortex_to_actors = sim.TsodyksMarkramSynapse(tau_facil = action_syn_tau_facil,
                                                         delay = action_syn_delay,
                                                         weight = weight_cortex_to_actors,
                                                         U = action_syn_U,
                                                         tau_rec = action_syn_tau_rec)
    

    # Create the Connections
    
    """Right Compound Eye"""
    
    # Nodes: Inputs: {0, 1} --> Outputs: {8}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[0]), CIRCUIT.id_to_index(CIRCUIT[1])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[8])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {2, 3} --> Outputs: {9}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[2]), CIRCUIT.id_to_index(CIRCUIT[3])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[9])])
    sim.Projection(presynaptic_population = PV(CIRCUIT, PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {4, 5} --> Outputs: {10}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[4]), CIRCUIT.id_to_index(CIRCUIT[5])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[10])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector=sim.AllToAllConnector(),
                   synapse_type=synapse_retinalphotoreceptor_to_lamina,
                   receptor_type='inhibitory')
    
    # Nodes: Inputs: {6, 7} --> Outputs: {11}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[6]), CIRCUIT.id_to_index(CIRCUIT[7])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[11])])
    sim.Projection(presynaptic_population =PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {8} --> Outputs: {12}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[8])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[12])])
    sim.Projection(presynaptic_population =PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {9} --> Outputs: {13}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[9])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[13])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {10} --> Outputs: {14}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[10])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[14])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {11} --> Outputs: {15}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[11])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[15])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {12} --> Outputs: {17}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[12])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[17])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_medula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {13, 14, 15} --> Outputs: {16}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[13]), CIRCUIT.id_to_index(CIRCUIT[14]), CIRCUIT.id_to_index(CIRCUIT[15])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[16])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_medula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {16} --> Outputs: {17}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[16])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[17])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_medula_to_medula,
                   receptor_type = 'excitatory')
    
    # # Nodes: Inputs: {17} --> Outputs: {18, 19}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[17])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[18]), CIRCUIT.id_to_index(CIRCUIT[19])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_medula_to_lobula,
                   receptor_type = 'excitatory')
    
    # # Nodes: Inputs: {19} --> Outputs: {18}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[19])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[18])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lobula_to_lobula,
                   receptor_type = 'inhibitory')
    
    # Nodes: Inputs: {18} --> Outputs: {20}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[18])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[20])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lobula_to_cortex,
                   receptor_type = 'excitatory')
    
    
    """Cortex and Motor Region"""
    
    # Nodes: Inputs: {20} --> Outputs: {21, 22}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[20])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[21]), CIRCUIT.id_to_index(CIRCUIT[22])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_cortex,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {20} --> Outputs: {19}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[20])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[19])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_lobula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {21} --> Outputs: {19}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[21])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[19])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_lobula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {21} --> Outputs {25}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[21])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[25])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_actors,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {22} --> Outputs {25, 26}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[22])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[25]), CIRCUIT.id_to_index(CIRCUIT[26])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_actors,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {24} --> Outputs {26}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[24])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[26])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_actors,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {22} --> Outputs: {21}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[22])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[21])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_cortex,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {22} --> Outputs: {24}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[22])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[24])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_cortex,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {23} --> Outputs: {22}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[23])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[22])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_cortex,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {23} --> Outputs: {24}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[23])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[24])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_cortex,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {23} --> Outputs: {27}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[23])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[27])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_lobula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {24} --> Outputs: {27}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[24])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[27])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_cortex_to_lobula,
                   receptor_type = 'excitatory')
    
    
    """Left Compound Eye"""
    
    # Nodes: Inputs: {39, 40} --> Outputs: {35}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[39]), CIRCUIT.id_to_index(CIRCUIT[40])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[35])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {41, 42} --> Outputs: {36}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[41]), CIRCUIT.id_to_index(CIRCUIT[42])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[36])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {43, 44} --> Outputs: {37}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[43]), CIRCUIT.id_to_index(CIRCUIT[44])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[37])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector=sim.AllToAllConnector(),
                   synapse_type=synapse_retinalphotoreceptor_to_lamina,
                   receptor_type='inhibitory')
    
    # Nodes: Inputs: {45, 46} --> Outputs: {38}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[45]), CIRCUIT.id_to_index(CIRCUIT[46])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[38])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_retinalphotoreceptor_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {35} --> Outputs: {31}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[35])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[31])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {36} --> Outputs: {32}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[36])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[32])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {37} --> Outputs: {33}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[37])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[33])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {38} --> Outputs: {34}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[38])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[34])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_lamina,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {31} --> Outputs: {29}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[31])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[29])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_medula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {32, 33, 34} --> Outputs: {30}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[32]), CIRCUIT.id_to_index(CIRCUIT[33]), CIRCUIT.id_to_index(CIRCUIT[34])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[30])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lamina_to_medula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {30} --> Outputs: {29}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[30])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[29])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_medula_to_medula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {29} --> Outputs: {27, 28}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[29])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[27]), CIRCUIT.id_to_index(CIRCUIT[28])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_medula_to_lobula,
                   receptor_type = 'excitatory')
    
    # Nodes: Inputs: {27} --> Outputs: {28}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[27])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[28])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lobula_to_lobula,
                   receptor_type = 'inhibitory')
    
    # Nodes: Inputs: {28} --> Outputs: {23}
    PreP = np.array([CIRCUIT.id_to_index(CIRCUIT[28])])
    PoP = np.array([CIRCUIT.id_to_index(CIRCUIT[23])])
    sim.Projection(presynaptic_population = PV(CIRCUIT,PreP),
                   postsynaptic_population = PV(CIRCUIT, PoP),
                   connector = sim.AllToAllConnector(),
                   synapse_type = synapse_lobula_to_cortex,
                   receptor_type = 'excitatory')
    
    
    sim.initialize(population, v=population.get('v_reset'))
    logger.debug("Circuit description: " + str(population.describe()))
    return CIRCUIT


circuit = create_brain()
sensors_righteye = circuit[0:19]
evaluators = circuit[20:24]
actors = circuit[25:26]
sensors_lefteye = circuit[27:46]
record = circuit[0:46]

