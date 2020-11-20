# -*- coding: utf-8 -*-
"""Modularity_global_local

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cfn23iYkcY3pvZaEUD7ox3O3ewve3iEc
"""

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

        self.l_modul_list = []
        self.g_modul_list = []

        self.t_modularity_list = []
        self.modularity = 0
        self.temp = temp
        self.f_comm = {}

        self.number_of_groups = number_of_groups

        # initial grouping with constrained number of groups
        self.comm = {node.index: np.random.randint(0, number_of_groups) for node in list(ntwk.vs())}  # two groups for now
        self.comms_set = list(set(self.comm.values()))

        num_comm = len(self.comms_set)

        while num_comm != self.number_of_groups :
          self.comm = {node.index: np.random.randint(0, number_of_groups) for node in list(ntwk.vs())}  # two groups for now
          self.comms_set = list(set(self.comm.values()))
          num_comm = len(self.comms_set)


        

    def GlobalMove(self, elligible):

        comm = self.comm
        # this is number of community
        # there is no empty group
        num_comm = 0 

        while num_comm != self.number_of_groups :
          
          node_choice = [i for i in range(2, len(elligible)+1)] #list of number for nodes being passed in 
          node_num = np.random.choice(node_choice)
          node_list = list(set(np.random.choice(elligible, node_num, replace=False))) #Take several random nodes (2~ length of elligible)

          s_node = np.random.choice(node_list) #select single node to check value
          selected = comm[s_node]
          new_comms_list = [val for val in self.comms_set if val != selected]

          #change values in all processing data
          change_comm = np.random.choice(new_comms_list) # number for new comm
          for node in node_list :
            comm[node] = change_comm
          
          num_comm = len(list(set(comm.values())))
          

        partition = ig.VertexClustering(self.ntwk, membership= list(comm.values()))
        gtemp_modularity = partition.q

        better = bool(gtemp_modularity >= self.modularity)
        temp_move = bool(np.random.rand() <= np.exp((gtemp_modularity - self.modularity) * (1/self.temp)))

        if better or temp_move :

          self.comm = comm
          self.modularity = gtemp_modularity
          self.t_modularity_list.append(gtemp_modularity)
          self.temp *= 0.995

          return True
        
        else:
          self.temp *=0.995

          return False

    def helper_GlobalMoves(self, g_elligible, num_moves=100,comm = {}, comm_choice=0, stop=5):
        num_moves = self.n
        comm = self.comm

        elligible = g_elligible
        g_len_elli = len(elligible) 
        
        while g_len_elli < 2 : #length of elligible for global movements at least 2
          comm_choice = np.random.choice(list(self.comms_set))
          elligible = [node for node, comm in self.comm.items() if comm == comm_choice]
          g_len_elli = len(elligible)

        for _ in range(num_moves) :
          val = self.GlobalMove(elligible)
          
          if val:  # check if need to consider the other community now

              comm_choice = np.random.choice(list(self.comms_set))
              self.g_modul_list.append(self.modularity)
              elligible = [node for node, comm in self.comm.items() if comm == comm_choice]  # redesignate which nodes are elligible

              g_len_elli = len(elligible)      
              while g_len_elli < 2 :
                  #print("AHHHHHHHHHHH")
                  comm_choice = np.random.choice(list(self.comms_set))
                  elligible = [node for node, comm in self.comm.items() if comm == comm_choice]
                  g_len_elli = len(elligible)

          else:
                continue

          
          f_comm = copy.deepcopy(comm)
          self.f_comm = f_comm
          elligible = copy.deepcopy(elligible)
          #print("g",self.g_modul_list[-1])
  

        #print("\n\n\n ~~~~~~~~~~~~~~~~~~ \n Final modularity is last {} \n community {} \n ~~~~~~~~~~~~~~~~~".format(modul_list[-1],final_comm))
        return self.f_comm, self.g_modul_list[-1], elligible                
          

    def LocalMove(self,elligible):
        # Make a copy to avoid prematurely altering "true" communities
        comm = self.comm

        # this is number of community
        # there is no empty group
        num_comm = 0
 
        while num_comm != self.number_of_groups :
          node = np.random.choice(elligible)  # Take a random node from the community being passed in
          
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
              new_comms_list = [val for val in self.comms_set if val != selected]
              comm[node] = np.random.choice(new_comms_list)
          
          num_comm = len(list(set(comm.values())))

        # Getting modularity of post-local move partitions
        partition = ig.VertexClustering(self.ntwk, membership=list(comm.values()))
        ltemp_modularity = partition.q

        # If move is better, adjust the community and modularity accordingly
        # Alternatively, if move is worse but succeed temperature calculations
        better = bool(ltemp_modularity >= self.modularity)
        temp_move = bool(np.random.rand() <= np.exp((ltemp_modularity - self.modularity) * (1 / self.temp)))

        if better or temp_move:
            self.comm = comm
            self.modularity = ltemp_modularity
            self.t_modularity_list.append(ltemp_modularity)
            self.temp *= 0.995

            return True
        else:
            self.temp *= 0.995
            return False

    def helper_LocalMoves(self,elligible, num_moves=100,comm = {}, comm_choice=0, stop=5):
        num_moves = (self.n) ** 2
        comm = self.comm

        # the set of nodes under a given community
        
        for _ in range(num_moves):
            val = self.LocalMove(elligible)
            #modularity_list_length = len(self.modularity_list)
            if val:  # check if need to consider the other community now

              
                comm_choice = np.random.choice(list(self.comms_set))
                self.l_modul_list.append(self.modularity)
                elligible = [node for node, comm in self.comm.items() if comm == comm_choice]  # redesignate which nodes are elligible
                    
                while not elligible:
                    #print("AHHHHHHHHHHH")
                    comm_choice = np.random.choice(list(self.comms_set))
                    elligible = [node for node, comm in self.comm.items() if comm == comm_choice]

            else:
                  continue
            
           
            f_comm = copy.deepcopy(comm)
            self.f_comm = f_comm
            elligible = copy.deepcopy(elligible)
            
            #print("l",self.l_modul_list[-1])
  
        #print(modul_list)
        #print("\n\n\n ~~~~~~~~~~~~~~~~~~ \n Final modularity is last {} \n community {} \n ~~~~~~~~~~~~~~~~~".format(modul_list[-1],final_comm))
        return self.f_comm, self.l_modul_list[-1], elligible

    def total_moves(self, stop, comm_choice =0) :

      start = time.time()
      modularity_repeat = True
      
      elligible = [node for node, comm in self.comm.items() if comm == comm_choice]

      modularity_list = []
      final_comm ={}

      while modularity_repeat == True :

        prob = np.random.rand()
        
        if prob  > 0.8 :
          local_comm, local_modul, new_l_elligible = self.helper_LocalMoves(elligible)
          elligible = new_l_elligible

        else :
          global_comm , global_modul, new_g_elligible = self.helper_GlobalMoves(elligible)
          elligible = new_g_elligible


        modularity_list_length = len(self.t_modularity_list)

        #print(self.modularity)
        if modularity_list_length >= stop :
            modularity_repeat = bool(len(set(self.t_modularity_list[-stop:])) != 1)
      
      end = time.time()
      print("\n\n\n ~~~~~~~~~~~~~~~~~~ \n Final modularity is last {} \n community {} \n  time    {}~~~~~~~~~~~~~~~~~".format(self.t_modularity_list[-1],self.f_comm, end-start))
      return self.t_modularity_list[-1]

G = ig.read('/content/karate.gml')

mod_list =[]
for _ in range(3) :
  Ann = Annealing(G, 4, temp = 99.5)
  mod = Ann.total_moves(stop = 100)
  mod_list.append(mod)




"""
n= 4, stop = 200 (only global move) 

~~~~~~~~~~~~~~~~~~ 
 Final modularity is last 0.41978961209730437 
 community {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 0, 8: 3, 9: 3, 10: 1, 11: 0, 12: 0, 13: 0, 14: 3, 15: 3, 16: 1, 17: 0, 18: 3, 19: 0, 20: 3, 21: 0, 22: 3, 23: 2, 24: 2, 25: 2, 26: 3, 27: 2, 28: 2, 29: 3, 30: 3, 31: 2, 32: 3, 33: 3} 
 ~~~~~~~~~~~~~~~~~
"""


