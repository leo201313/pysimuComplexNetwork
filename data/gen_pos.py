import json
import networkx as nx
import numpy as np

data_addr = "./facebook_combined.txt"
G_fb = nx.read_edgelist(data_addr, create_using = nx.Graph(), nodetype=int)
ps = nx.spring_layout(G_fb)


pos_dic = {}

for node,pos in ps.items():
    pos_dic[node] = list(pos)


filename = 'facebook_combined.json'
with open(filename,'w') as f_obj:
    json.dump(pos_dic,f_obj)

