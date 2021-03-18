import networkx as nx
import matplotlib.pyplot as plt

G_fb = nx.read_edgelist("./data/facebook_combined.txt", create_using = nx.Graph(), nodetype=int)
print(nx.info(G_fb))

# if need drawing
ps = nx.spring_layout(G_fb)
nx.draw(G_fb, ps, with_labels = False, node_size = 5)
plt.show()

# ps = nx.spring_layout(G_fb)
# betCent = nx.betweenness_centrality(G_fb, normalized=True, endpoints=True)
# node_color = [20000.0 * G_fb.degree(v) for v in G_fb]
# node_size =  [v * 10000 for v in betCent.values()]
# plt.figure(figsize=(20,20))
# nx.draw_networkx(G_fb, pos=ps, with_labels=False,
#                  node_color=node_color,
#                  node_size=node_size )
# plt.axis('off')