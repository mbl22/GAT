import networkx as nx
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

def load_country(country):

    attr_list = []
    edge_list = []
    init_list = []
    data_frame_list = (pd.read_excel(f"World Bank Data {country}.xlsx"),
                     pd.read_excel(f"CIRI {country}.xlsx"),
                     pd.read_excel(f"DPI {country}.xlsx"))
    df = pd.concat(data_frame_list)
    header_list = df.columns.values.tolist()
    country_dict = df.to_dict(orient='index')
    y = len(country_dict)
    # iterate through data set and assign PMESII points to weighted edge lists
    for val in range(0, y):
        edge_list.append((country_dict[val]['Variable Code'], country_dict[val]['Domain']))
        edge_list.append((country_dict[val]['Domain'], 'PMESII Resources'))
        for y in range(1975, 1979):
            if country_dict[val][y] != str(country_dict[val][y]):
                init_list.append(country_dict[val][y])
                attr_list.append((country_dict[val]['Variable Code'],
                                  country_dict[val]['Domain'],
                                  np.mean(init_list)))
                init_list = []
    pmesii_graph = nx.Graph()
    pmesii_graph.add_weighted_edges_from(attr_list, 'W')
    print(nx.info(pmesii_graph))
    return pmesii_graph

