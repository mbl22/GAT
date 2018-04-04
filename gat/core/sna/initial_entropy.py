import networkx as nx
from sna import SNA
from sklearn.metrics.cluster import mutual_info_score
import numpy as np
import random
from community_louvain import best_partition
from collections import defaultdict

'''
Step 1: find partition p_0 by optimizing community modularity.
input: 
    -The undirected graph G
    -an SNA headerlist
    -a dictionary of centralities for each node in G
output: each modularity-optimized partition with an initial entropy value as a dictionary attribute for each node
'''

def initial_entropy(G, headerList, centralities, weightKey='emoWeight'):

    partition = best_partition(u, weight=weightKey)
    partitions = defaultdict(list)
    subgraphs = []
    partitionLists = []
    shannon_entropy_steps = []
    initial_entropy_list = []
    node_1_info_vector =[]
    node_2_info_vector = []
    if centralities is not None:
        for node, partitionKey in partition.items():
            partitions[partitionKey].append(node)
            partitionLists = [nodes for partition, nodes in partitions.items()]
        for partition in partitionLists:
            node_data = [d for n, d in G.nodes_iter(data=True) if n in partition]
            for node_1 in range(0, len(node_data)):
                for node_2 in range(0, len(node_data)):
                    for attr in headerList:
                        if attr in node_data[node_1] and attr in node_data[node_2] and \
                                        node_data[node_1][attr][0] == node_data[node_2][attr][0] and \
                                        node_data[node_1]['Name'] != node_data[node_2]['Name']:
                            for x in node_data[node_1][attr]:
                                if 'W' in x[1]:
                                    node_1_info_vector.append(x[1]['W'])
                            for y in node_data[node_2][attr]:
                                if 'W' in y[1]:
                                    node_2_info_vector.append(y[1]['W'])
                            if len(node_1_info_vector) == len(node_2_info_vector):
                                node_pair_info_score = mutual_info_score(node_1_info_vector, node_2_info_vector)
                                shannon_entropy_step = 1 / (node_pair_info_score * np.log(node_pair_info_score) +
                                                            (1 - node_pair_info_score) * np.log(node_pair_info_score))
                                if shannon_entropy_step == shannon_entropy_step: # eliminating NaN results
                                    shannon_entropy_steps.append(shannon_entropy_step)
            partition_entropy = np.sum(shannon_entropy_steps)
            initial_entropy_list.append([partition_entropy, partition])
            nx.set_node_attributes((G.subgraph(partition)), 'Entropy', partition_entropy)
            subgraphs.append(G.subgraph(partition))

        return subgraphs
    else:
        return "No centralities passed"