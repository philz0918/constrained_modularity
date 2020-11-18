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
import copy

# Custom

# ----------------------------
__author__ = "Daniel Kaiser"
__credits__ = ["Daniel Kaiser", "Sangpil Youm"]

__version__ = "0.1"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ====================== CLASSES AND FUNCTIONS =======================
class Annealing:
    '''Class to handle the network data to perform constrained SA on'''

    def __init__(self, ntwk, number_of_groups):
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
        self.n = ntwk.number_of_nodes()
        self.temp = 100
        self.modularity = 0
        self.modularity_list = []

        # initial grouping with constrained number of groups
        self.comm = {node: np.random.randint(0, number_of_groups) for node in list(ntwk.nodes())}  # two groups for now
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
        Q_comms = [{x for x, y in comm.items() if y == c} for c in set(comm.values())]  # formatting for nx function
        modularity = nx.algorithms.community.modularity(self.ntwk, Q_comms)

        # If move is better, adjust the community and modularity accordingly
        # Alternatively, if move is worse but succeed temperature calculations
        better = bool(modularity >= self.modularity)
        temp_move = bool(np.random.rand() <= np.exp((modularity - self.modularity) * (1 / self.temp)))

        if better or temp_move:
            self.comm = comm
            self.modularity = modularity
            self.modularity_list.append(modularity)
            self.temp *= 0.9
            print("Temperature:", self.temp)
            return True
        else:
            self.temp *= 0.9
            return False

    def helper_LocalMoves(self, num_moves=100, comm={}, comm_choice=0):
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
                    #fix here
                    print("This is length of modul list : ", modularity_list_length)
                    if modularity_list_length >= 5 :
                        modularity_repeat = bool(len(set(self.modularity_list[-5:])) != 1)

                else:
                    continue

                final_comm = comm

                print("Stopping condition,", modularity_repeat)
                print(comm)
                print(final_comm)

                final_comm = copy.deepcopy(final_comm)
                print("Max modularity currently: ", max(modul_list))


        print("Final modularity is last {} \n community {}".format(modul_list[-1],final_comm))

if __name__ == '__main__':
    G = nx.read_gml('sourcefile/karate.gml', 'id')
    Ann = Annealing(G, 2)
    Ann.helper_LocalMoves()



