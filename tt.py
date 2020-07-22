import numpy.random as random
import numpy as np
import math
import networkx as nx
from scipy import sparse as sp
import random


def read_pairs_file(pairfile):
    file = open(pairfile, "r")

    edges = []
    weights = []

    for line in file:
        nodes = line.split()
        edges.append((nodes[0], nodes[1]))

        # weight
        if len(nodes) == 3:
            weights.append(float(nodes[2]))
        else:
            weights.append(1.0)
    file.close()

    pair_dict = {}
    t_num = 0

    for edge in edges:
        if edge[0] not in pair_dict:
            pair_dict[edge[0]] = t_num
            t_num += 1
        if edge[1] not in pair_dict:
            pair_dict[edge[1]] = t_num
            t_num += 1

    adj = []

    adj.extend([[pair_dict[edge[0]], pair_dict[edge[1]]] for edge in edges])
    adj.extend([[pair_dict[edge[1]], pair_dict[edge[0]]] for edge in edges])

    print(adj)
    adj = np.array(adj).transpose()

    weights.extend(weights)
    w_mat = np.array(weights)

    n = t_num  # number of nodes
    # print(n)
    # print(w_mat)
    # print(adj)

    A_mat = sp.csr_matrix((w_mat, adj), shape=(n, n))

    # number of nodes
    n_A = A_mat
    sumit = A_mat.sum()
    m = (sumit / 2)  # number of edge
    return n, n_A, m


## we need network


# n is number of elements, cn, constrainumber
def initial_grouping(n, cn):
    # get list of nodes
    nodes = [node for node in range(0, n)]

    # assign group number to each nodes
    group_assign = [random.randrange(0, cn) for g_num in range(len(nodes))]

    return nodes, group_assign


# partition is group-assigned list
def partition_matrix(partition):
    n = len(partition)
    data = np.ones(n)
    # print(data)
    ij = np.array([partition, list(range(0, n))])
    # print(ij)
    grouping_matrix = sp.csr_matrix((data, ij))
    return grouping_matrix


# s = partition matrix, k = degree matrix , m = number of edge


def degree_matrix(adj):
    d_mat = n_A.sum(axis=1)
    return d_mat


def modularity_mat(adj, k, m):
    null_model = np.dot(k, k.transpose()) / (2 * m)

    m_m = (adj - null_model)

    return m_m


def get_modularity(adj, s, k, m):
    # formula modularity = (Adj * p_matrix - (d_matrix)^2 * p_matrix/2m) / 2m

    adj_partition = (s * adj * s.transpose()).diagonal().sum()
    deg_par = np.array(s * k)
    degree_partition = np.square(deg_par).sum() / (2 * m)

    # modularity
    Q = (adj_partition - degree_partition) / (2 * m)

    return Q


def patching(group_list, cn):
    n_nodes = len(group_list)
    # cn is constrained number of groups
    n_groups = cn
    # get index and value that want to change

    idx = random.choice([x for x in range(0, n_nodes)])
    val = group_list[idx]

    n_val = random.choice([y for y in range(0, n_groups) if y != val])

    group_list[idx] = n_val
    patched_group = group_list

    return patched_group


def annealing_simulating(initial_temp, adj, n, cn, s, k, m, cooling_constant, iteration):
    svg_group_list = []
    modul_list = []
    old_Q = None

    for i in range(iteration):

        temp = new_temp(cooling_constant, initial_temp, i)
        acceptance = False
        num_rejection = -1
        # n numberof nodes, cn constrained number of groups
        rej_threshold = cal_rej_thres(n, cn)
        # print(rej_threshold)

        while acceptance is False:

            num_rejection += 1
            # print(old_Q)

            if old_Q is None:
                old_Q = get_modularity(adj, s, k, m)

            # patching new grouping list
            new_grouping = patching(group_list, cn)
            print(new_grouping)
            # new grouping matrix
            new_s = partition_matrix(new_grouping)
            # new modularity with new grouping matrix
            new_Q = get_modularity(adj, new_s, k, m)
            print(new_Q)
            acceptance = check_acceptance(old_Q, new_Q, temp)

            # print(num_rejection)
            if num_rejection > rej_threshold:
                break

            if acceptance is True:

                if new_grouping in svg_group_list:
                    acceptance = False
                else:
                    svg_group_list.append(new_grouping)
                    modul_list.append(new_Q)
                    print(new_Q)
                    old_Q = new_Q

    opt_grouping = svg_format(new_grouping)
    opt_modul = new_Q

    return opt_grouping, opt_modul


def new_temp(cooling_constant, prev_temp, times):
    new_temp = (math.pow(cooling_constant, times)) * prev_temp
    return new_temp


def check_acceptance(modul_old, modul_new, temp):
    if modul_new > modul_old:
        return True
    else:
        new_accept = math.exp((modul_new - modul_old) * temp)
        # modul_new- modul_old is negative value
        # when temp is higher , new_accept is getting smaller
    return (np.random.random_sample() < new_accept)  # get true or false


def cal_rej_thres(n, nc):
    num_pathing = n * nc

    num_of_moves = num_pathing

    confi = 1 - math.log(0.05) / math.log(num_of_moves)

    return confi * num_of_moves * math.log(num_of_moves)


def svg_format(group_list):
    fin_set = {}
    for idx, gnum in enumerate(group_list):
        if gnum in fin_set:
            fin_set[gnum].append(idx)
        else:
            fin_set[gnum] = [idx]
    return fin_set


class OptimumReached(Exception):
    def __init__(self, time_step):
        self.time_step = time_step

    def __str__(self):
        return "Optimum reached at step %d" % self.time_step

a = [0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1]
n, n_A, m=read_pairs_file("karate.pairs")
#node_list, group_list = initial_grouping(n,2)
k = degree_matrix(n_A)
s = partition_matrix(a)

print(n_A.toarray())
