import networkx as nx
import matplotlib.pyplot as plt

ws = nx.random_graphs.watts_strogatz_graph(50, 10, 0.4)
ps = nx.spring_layout(ws)
nx.draw(ws, ps, with_labels = False, node_size = 50)
plt.show()
