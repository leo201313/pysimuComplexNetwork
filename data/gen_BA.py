import networkx as nx
import json
import matplotlib.pyplot as plt

ba = nx.barabasi_albert_graph(500, 1)

# if need drawing
ps = nx.spring_layout(ba)
nx.write_edgelist(ba, "ba500.txt")

pos_dic = {}

for node,pos in ps.items():
    pos_dic[node] = list(pos)


filename = 'ba500.json'
with open(filename,'w') as f_obj:
    json.dump(pos_dic,f_obj)

nx.draw(ba, ps, with_labels = False, node_size = 10)
plt.show()
