import networkx as nx
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

# defining which country plays which role per year within the Phoenix dataset:
role_dict = {}
for i in list(['USA', 'RUS', 'USSR', 'TUR', 'IRN', 'KSA', 'CHN', 'FRA', 'GER', 'GBR', 'CAN', 'IRQ', 'SYR', 'GRC']):
    role_dict[i] = {1945: '', 1991: '', 2013: ''}
role_dict['USA'][1945] = 'HEG'
role_dict['USA'][1991] = 'HEG'
role_dict['USA'][2013] = 'HEG'
role_dict['RUS'][1945] = 'HEG'
role_dict['RUS'][1991] = 'REV'
role_dict['RUS'][2013] = 'REV'
role_dict['TUR'][1945] = 'ALY'
role_dict['TUR'][1991] = 'ALY'
role_dict['TUR'][2013] = 'DEF'
role_dict['IRN'][1945] = 'REV'
role_dict['IRN'][1991] = 'REV'
role_dict['IRN'][2013] = 'DOF'
role_dict['KSA'][1945] = 'ALY'
role_dict['KSA'][1991] = 'DOF'
role_dict['KSA'][2013] = 'DOF'
role_dict['CHN'][1945] = 'ISO'
role_dict['CHN'][1991] = 'ISO'
role_dict['CHN'][2013] = 'IND'
role_dict['FRA'][1945] = 'ALY'
role_dict['FRA'][1991] = 'ALY'
role_dict['FRA'][2013] = 'ALY'
role_dict['GER'][1945] = 'ALY'
role_dict['GER'][1991] = 'ALY'
role_dict['GER'][2013] = 'MED'
role_dict['GBR'][1945] = 'ALY'
role_dict['GBR'][1991] = 'ALY'
role_dict['GBR'][2013] = 'ALY'
role_dict['CAN'][1945] = 'ALY'
role_dict['CAN'][1991] = 'ALY'
role_dict['CAN'][2013] = 'ALY'
role_dict['IRQ'][1945] = 'ALY'
role_dict['IRQ'][1991] = 'DEP'
role_dict['IRQ'][2013] = 'DEP'
role_dict['SYR'][1945] = 'IND'
role_dict['SYR'][1991] = 'IND'
role_dict['SYR'][2013] = 'DEP'
role_dict['GRC'][1945] = 'ALY'
role_dict['GRC'][1991] = 'ALY'
role_dict['GRC'][2013] = 'DEP'


def find_role(source, year, month):
    if year < 1991:
        year = 1945
    elif year < 2013:
        year = 1991
    else:
        year = 2013
    if source not in role_dict:
        return False
    return role_dict[source][year]


def generate(phoenix_data):
    output_file = "Phoenix_A.txt"
    ofile = open(output_file, 'wb')
    writer = csv.writer(ofile, delimiter=',')

    with open(phoenix_data, 'rU') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',')
        headers = my_reader.next()

        # relevant indicies
        year = headers.index('year')
        month = headers.index('month')
        source = headers.index('source_root')
        target = headers.index('target_root')
        move = headers.index('code')

        for event in my_reader:
            role = find_role(event[source], event[year], event[month])
            if role == False:
                continue
            if len(event[move]) == 2:
                print(event[move])
            prefix = event[move][:2]
            row = event
            row.append(role)
            row.append(prefix)
            writer.writerow(row)

# output is a dictionary of the amount of times
def stats(updated_data):
    global counts_by_role
    global counts_by_move
    counts_by_role = {}
    counts_by_move = {}

    with open(updated_data, 'rU') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',')

        for event in my_reader:
            if len(event[26]) == 1:
                print(event[26])
            if event[25] not in counts_by_role:
                counts_by_role[event[25]] = {}
            if event[26] not in counts_by_role[event[25]]:
                counts_by_role[event[25]][event[26]] = 0
            if event[26] not in counts_by_move:
                counts_by_move[event[26]] = {}
            if event[25] not in counts_by_move[event[26]]:
                counts_by_move[event[26]][event[25]] = 0
            counts_by_role[event[25]][event[26]] += 1
            counts_by_move[event[26]][event[25]] += 1

        return counts_by_role


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

G = load_country('Iran')
tm_force = [('MS.MIL.XPND.CN', 'MS.MIL.TOTL.P1', G['Military']['MS.MIL.XPND.CN']['W']),
            ('MS.MIL.MPRT.KD', 'MS.MIL.TOTL.P1', G['Military']['MS.MIL.MPRT.KD']['W'])]

tm_messaging = [('IT.NET.SECR', 'IT.NET.USER.ZS', G['Information']['IT.NET.SECR']['W']),
                ('BX.GSR.CMCP.ZS', 'IT.NET.SECR', G['Economic']['BX.GSR.CMCP.ZS']['W'])]

tm_build = [('NY.GDP.MKTP.KD', 'IS.RRS.GOOD.MT.K6', G['Economic']['NY.GDP.MKTP.KD']['W']),
            ('IS.RRS.GOOD.MT.K6', 'SL.IND.EMPL.ZS', G['Infrastructure']['IS.RRS.GOOD.MT.K6']['W']),
            ('SL.IND.EMPL.ZS', 'EG.GDP.PUSE.KO.PP.KD', G['Economic']['SL.IND.EMPL.ZS']['W'])]

tm_invest = [('NY.GDP.MKTP.KD', 'GC.TAX.TOTL.CN', G['Economic']['NY.GDP.MKTP.KD']['W']),
             ('GC.TAX.TOTL.CN', 'GC.NFN.TOTL.CN', G['Economic']['GC.TAX.TOTL.CN']['W']),
             ('GC.NFN.TOTL.CN', 'BM.KLT.DINV.CD.WD', G['Economic']['GC.NFN.TOTL.CN']['W'])]


force_types = ['Assault', 'Fight', 'Use conventional mass violence', 'Coerce', 'Exhibit force posture',
                'Reduce relations', 'Threaten', 'Reject', 'Disapprove', 'Investigate', 'Protest',
                'Refuse to build infrastructure', 'Demand', 'Demand to build infrastructure']
messaging_types = ['Reduce relations', 'Reject', 'Disapprove', 'Investigate', 'Protest',
                   'Refuse to build infrastructure', 'Appeal', 'Demand', 'Make a public statement',
                   'Express intent',
                   'Appeal to build infrastructure', 'Express intent to cooperate',
                   'Express intent to build infrastructure', 'Consult', 'Engage in diplomatic cooperation',
                   'Use social following', 'Control information', 'Build social infrastructure',
                   'Build political infrastructure', 'Build information infrastructure']
build_types = ['Appeal to build infrastructure', 'Express intent to build infrastructure',
               'Engage in material cooperation', 'Build energy infrastructure', 'Build social infrastructure',
               'Build political infrastructure', 'Build military infrastructure',
                'Build information infrastructure',
                'Build economic infrastructure', 'Gather/mine for materials']
invest_types = ['Provide aid', 'Build economic infrastructure', 'Change price', 'Government funds']

force_list = []
messaging_list = []
build_list = []
invest_list = []
cameo_arch = (pd.read_excel("CAMEO_arch.xlsx"))
cameo_headerList = cameo_arch.columns.values.tolist()
cameo_dict = cameo_arch.to_dict(orient='index')
print(cameo_dict)
for val in range(0, len(cameo_dict)):
    if cameo_dict[val]['Type'] in force_types:
        force_list.append(cameo_dict[val]['Code'])
    if cameo_dict[val]['Type'] in messaging_types:
        messaging_list.append(cameo_dict[val]['Code'])
    if cameo_dict[val]['Type'] in build_types:
        build_list.append(cameo_dict[val]['Code'])
    if cameo_dict[val]['Type'] in invest_types:
        invest_list.append(cameo_dict[val]['Code'])


stats_dict = stats('/Users/ml/Projects/PycharmProjects/CAMEO/Phoenix_A.txt')
role_prob_list = []
for rm in stats_dict:

    buckets = []
    vals = []
    prob_dict = {}
    for item in stats_dict[rm]:
        buckets.append(float(item))
        vals.append(stats_dict[rm][item])

    bucket_sum = sum(buckets)
    for x in range(0, len(vals)):
        bucket_prob = (buckets[x] / bucket_sum)
        prob_dict[vals[x]] = bucket_prob

VC_iran = nx.DiGraph()
VC_iran.add_weighted_edges_from(tm_force)
VC_iran.add_weighted_edges_from(tm_messaging)
VC_iran.add_weighted_edges_from(tm_build)
VC_iran.add_weighted_edges_from(tm_invest)
print(nx.info(VC_iran))




