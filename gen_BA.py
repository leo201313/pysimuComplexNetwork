import networkx as nx
import matplotlib.pyplot as plt

ba = nx.barabasi_albert_graph(300, 1)

# if need drawing
ps = nx.spring_layout(ba)
nx.draw(ba, ps, with_labels = False, node_size = 50)
plt.show()
