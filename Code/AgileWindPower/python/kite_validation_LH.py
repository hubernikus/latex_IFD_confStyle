# -*- coding: utf-8 -*-
"""###########################################################################
#
#                   kite validation script
#                     klh   
#
########################################################################### """

print('Kite validation started')

# Import needed libraries
import numpy as np # Basic math library

from sys import path
import matplotlib.pyplot as plt

# Import ReadYalm
path.append("/home/lukas/Software/casadi/casadi-py35-np1.9.1-v3.2.3-64bit")
from casadi import *

# Personal functions
from kite_sim import *
#import quatlib

## CLASS definitions 
#class SimulationParameters:
#    """Class of Simulation Parameters"""
#    
#
#class Aerodynamics:    
#    """Class of the Aerodynamics of FlyingObjects"""
#    
#class Geometry:
#    """Class of the Geometry of Flying Vehicles"""
#    def __init__(self):
#        return
#
#class FlyingVehicle:
#    """Class of Flying Vehicles"""
#    def __init__(self):
#        aerodynamic = Aerodynamics();
#        geometry = Geometry();

  
#create kite model
#aircraft = yaml.read('umx_radian.yaml');

#YAML_stream = open('umx_radian.yaml')
 #aircraft = yaml.load_all(YAML_stream)


import yaml # import yaml files
with open('umx_radian.yaml') as yamlFile:
    aircraft = yaml.safe_load(yamlFile)
    
#for doc in docs:
#    for k,v in doc.items():
#        print( k, "->", v, '\n')
#    print("\n")

parameters = dict()

parameters['simulation'] = 0
parameters['plot'] = 0
parameters['vr'] = 0
parameters['int_type'] = 'cvodes'

start_sample = 10
# s_time = exp_telemetry(start_sample,end)
# f_time = exp_telemetry(end,end)
# parameters['t_span'] = [s_time, f_time, dt]
# parameters['x0'] = exp_telemetry(start_sample,1:13)'
parameters['u0'] = np.array([0,0,0])

## Start simulation
[num, flog, sym] = kite_sim(aircraft, parameters)
