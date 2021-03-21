import networkx as nx
import json
import matplotlib.pyplot as plt

ws = nx.random_graphs.watts_strogatz_graph(50, 5, 0.4)
ps = nx.spring_layout(ws)

nx.write_edgelist(ws, "ws50.txt")

pos_dic = {}

for node,pos in ps.items():
    pos_dic[node] = list(pos)


filename = 'ws50.json'
with open(filename,'w') as f_obj:
    json.dump(pos_dic,f_obj)




nx.draw(ws, ps, with_labels = False, node_size = 50)
plt.show()
