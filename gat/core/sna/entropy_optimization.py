import networkx as nx
from sklearn.metrics.cluster import mutual_info_score
import numpy as np
import random
from collections import defaultdict
from initial_entropy import initial_entropy

'''
Step 2: find partition p_0 by optimizing community modularity.
input: 
    -The undirected graph G
    -an SNA headerlist
output: each modularity-optimized and entropy-optimized partition with an initial entropy value as a 
dictionary attribute for each node.
'''

def entropy_optimization(graph, headerList):

    partitions = defaultdict(list)
    initial_entropy_list = []
    shannon_entropy_seconds = []
    node_1_info_vector = []
    node_2_info_vector = []
    subgraphs = initial_entropy(graph, headerList, centralities=nx.eigenvector_centrality(graph))
    for subgraph in subgraphs:
        backup = subgraph.copy()
        node_data = [d for n, d in graph.nodes_iter(data=True) if n in subgraph]
        for node in subgraph.copy():
            random_part = random.randint(0, len(subgraphs) - 1)
            subgraph.remove_node(node)
            subgraphs[random_part].add_node(node)
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
                                if shannon_entropy_step == shannon_entropy_step:  # eliminating NaN results
                                    shannon_entropy_seconds.append(shannon_entropy_step)
            partition_entropy = np.sum(shannon_entropy_seconds)
            initial_entropy_list.append([partition_entropy, subgraph])
            h = (nx.get_node_attributes(subgraph, 'Entropy'))
            d = list(h.values())
            if partition_entropy > np.mean(d):
                subgraph = backup
            else:
                nx.set_node_attributes(subgraph, 'Entropy', partition_entropy)
        return subgraphs

