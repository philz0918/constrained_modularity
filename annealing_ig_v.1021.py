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

# debugging
import time

# External
import igraph as ig
import numpy as np
import copy
import pandas as pd

# Custom

# ----------------------------
__author__ = ["Daniel Kaiser", "Sangpil Youm"]
__credits__ = ["Daniel Kaiser", "Sangpil Youm"]

__version__ = "0.4"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ====================== CLASSES AND FUNCTIONS =======================
class Annealing:
    '''Class to handle the network data to perform constrained SA on'''

    def __init__(self, ntwk, number_of_groups, temp):
        '''Constructor for SANetwork class
        Inputs :
            ntwk : networkx Network
                ntwk is a networkx Network class objct
            number_of_groups : positive int
                The number of communities to find
        Returns :
            None
        '''
        self.ntwk = ntwk
        self.n = ntwk.vcount()
        self.temp = temp
        self.modularity = 0
        self.modularity_list = []

        # initial grouping with constrained number of groups
        self.comm = {node.index: np.random.randint(0, number_of_groups) for node in list(ntwk.vs())}  # two groups for now
        # fix here by sangpil
        self.comms_set = list(set(self.comm.values()))
        self.number_of_groups = number_of_groups

    def GlobalMove(self, num_moves=100):
        pass

    def LocalMove(self, elligible):
        node = np.random.choice(elligible)  # Take a random node from the community being passed in
        comm = self.comm  # Make a copy to avoid prematurely altering "true" communities

        # Making the local move
        new_comms = set(comm.values())

        # two cases one for all nodes has same comm, and others not
        # fix here by sangpil
        if len(new_comms) == 1:
            selected = comm[node]
            # get from ground truth set of comms
            new_comms_list = [val for val in self.comms_set if val != selected]
            comm[node] = np.random.choice(new_comms_list)
        else:
            selected = comm[node]
            new_comms_list = [val for val in new_comms if val != selected]
            comm[node] = np.random.choice(new_comms_list)

        # Getting modularity of post-local move partitions
        partition = ig.VertexClustering(self.ntwk, membership=list(comm.values()))
        modularity = partition.q

        # If move is better, adjust the community and modularity accordingly
        # Alternatively, if move is worse but succeed temperature calculations
        better = bool(modularity >= self.modularity)
        temp_move = bool(np.random.rand() <= np.exp((modularity - self.modularity) * (1 / self.temp)))

        if better or temp_move:
            self.comm = comm
            self.modularity = modularity
            self.modularity_list.append(modularity)
            self.temp *= 0.995
            #print("Temperature:", self.temp)
            return True
        else:
            self.temp *= 0.995
            return False

    def helper_LocalMoves(self, num_moves=100, comm={}, comm_choice=0, stop=5):
        num_moves = (self.n) ** 2
        comm = self.comm

        # the set of nodes under a given community
        elligible = [node for node, comm in self.comm.items() if comm == comm_choice]

        modul_list = []
        modularity_repeat = True
        final_comm = None

        while modularity_repeat == True :
            for _ in range(num_moves):
                val = self.LocalMove(elligible)
                modularity_list_length = len(self.modularity_list)
                if val:  # check if need to consider the other community now

                    ##fix here by sangpil
                    comm_choice = np.random.choice(list(self.comms_set))
                    modul_list.append(self.modularity)
                    elligible = [node for node, comm in self.comm.items() if
                                 comm == comm_choice]  # redesignate which nodes are elligible
                    
                    while not elligible:
                        print("AHHHHHHHHHHH")
                        comm_choice = np.random.choice(list(self.comms_set))
                        elligible = [node for node, comm in self.comm.items() if
                                 comm == comm_choice]


                    #fix here 1015
                    if modularity_list_length >= stop :
                        modularity_repeat = bool(len(set(self.modularity_list[-stop:])) != 1)

                else:
                    continue

                final_comm = comm
                final_comm = copy.deepcopy(final_comm)

                print("Max modularity currently: ", max(modul_list))


        print("\n\n\n ~~~~~~~~~~~~~~~~~~ \n Final modularity is last {} \n community {} \n ~~~~~~~~~~~~~~~~~".format(modul_list[-1],final_comm))
        return max(modul_list)

if __name__ == '__main__':
    # Read in graph
    G = ig.read('sourcefile/karate.gml')


    mods = []
    stops = []
    times = []
    temps = []

    for _ in range(100):    
        for stop in [5,6,7,8,9,10]:
            for temp in [99.5,99,95,90]:
                # debug timer
                timer = time.time()

                # declare annelaing class and run
                Ann = Annealing(G, 2, temp=temp)
                mod = Ann.helper_LocalMoves(stop=stop)    
                
            
                # debug prints
                print("\n\n\n Run took {} seconds\n\n\n\n\n\n\n".format(time.time()-timer))

                # save data
                mods.append(mod)
                stops.append(stop)
                times.append(time.time()-timer)
                temps.append(temp)

    df = pd.DataFrame({
        "modularity" : mods,
        "stopping condition" : stops,
        "time" : times,
        "temp": temps
    })

    df.to_csv('test.csv')

    df.hist(modularity, groupby='stopping condition')