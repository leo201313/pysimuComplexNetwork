import networkx as nx
import random

random.seed(2021)

############### Hyper Constant ##################
HEALTH_TRESHOLD = 50


class Node(object):
    def __init__(self):
        self.id_list = []
        self.load = {}   # roughly related to degree-centrality
        self.append_load = {}
        self.load_capacity = {}   # 1.5 * load
        self.health = {}
        self.attack_cost = {}   # roughly related to degree-centrality
        self.recovery_ability = {} # roughly related to clustering
        self.state = {} # 1 is well served, 0 is defeated and recovery, 2 is overload malfunction
        self.degree = {}
        self.num = 0

    def ini(self,graph,load_lst):
        self.id_list = list(graph.nodes)
        self.num = len(self.id_list)
        self.load = load_lst
        node_degree = dict(graph.degree)
        self.degree = node_degree

        degree_centrality = dict(nx.degree_centrality(graph))
        max_degree_node = max(degree_centrality,key=degree_centrality.get)
        min_degree_node = min(degree_centrality,key=degree_centrality.get)
        degree_delta = degree_centrality[max_degree_node] - degree_centrality[min_degree_node]

        clustering = dict(nx.clustering(graph))
        max_clustering = max(clustering,key=clustering.get)
        min_clustering = min(clustering, key=clustering.get)
        clustering_delta = clustering[max_clustering] - clustering[min_clustering]

        for nodeid in self.id_list:
            self.health[nodeid] = 100
            self.state[nodeid] = 1
            self.append_load[nodeid] = 0

            load_capacity = int(abs(random.normalvariate(100,20)) + 1.2*self.load[nodeid])
            self.load_capacity[nodeid] = load_capacity

            attack_cost = 10 + abs(random.normalvariate(20,5)) + \
                          200 * (degree_centrality[nodeid] - degree_centrality[min_degree_node]) / degree_delta
            attack_cost = int(attack_cost)
            self.attack_cost[nodeid] = attack_cost

            if clustering_delta==0:
                recovery = abs(random.normalvariate(9, 3))
            else:
                recovery = abs(random.normalvariate(9,3)) + 16 * (clustering[nodeid] - clustering[min_clustering]) / clustering_delta
            recovery = int(recovery)
            self.recovery_ability[nodeid] = recovery











