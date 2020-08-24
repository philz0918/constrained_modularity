#!/usr/bin/env python
'''
Module to handle constrained simulated annealing calculations for community detection in complex networks. 
'''

# ================================= IMPORTS ==============================
# Built-ins
import os
import sys
import pickle
import random

# External
import networkx as nx
import numpy as np

# Custom

# ----------------------------
__author__ = "Daniel Kaiser"
__credits__ = ["Daniel Kaiser", "Sangpil Youm"]

__version__ = "0.1"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"

# ====================== CLASSES AND FUNCTIONS =======================
class SANetwork:
    '''Class to handle the network data to perform constrained SA on'''

    def __init__(self, fh):
        '''Constructor for SANetwork class

        Inputs : 
            fh : string
                fh is a path string to a .gml network file
        
        Returns :
            None
        '''
        self.fh = nx.read_gml(fh)