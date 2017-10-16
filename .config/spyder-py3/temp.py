# -*- coding: utf-8 -*-
"""###########################################################################
#
#                   kite validation script
#                     klh   
#
########################################################################### """

# clear all; ## To ensure clean workspace
##
# clc; close all; clear variables;

# Import needed libraries
import numpy as np # Basic math library
import yaml # import yaml files

from sys import path

# Import ReadYalm
path.append("/home/lukas/Software/casadi/casadi-py35-np1.9.1-v3.2.3-64bit")
from casadi import *

class TestClass:
    x =1
    
class Test2Class:
    y = 32
    
Instance1 = TestClass()


Instance1.yy = Test2Class()

Instance1.z = 1

Instance1.yy.xx = 10

spanish = dict()
spanish['hello'] = 'hola'
spanish['yes'] = 'si'
spanish['one'] = 'uno'
spanish['two'] = 'dos'
spanish['three'] = 'tres'
spanish['red'] = 'rojo'
spanish['black'] = 'negro'
spanish['green'] = 'verde'
spanish['blue'] = 'azul'

print(spanish['two'])
print(spanish['red'])

 
print('End shizzle')    