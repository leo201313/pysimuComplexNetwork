import networkx as nx

############### Hyper Constant ##################
HEALTH_TRESHOLD = 50




class Node(object):
    def __init__(self):
        self.id_list = []
        self.load = {}   # roughly related to degree
        self.health = {}
        self.attack_cost = {}  # roughly related to local clustering
        self.recovery_ability = {}
        self.state = {} # 0 is well served, 1 is defeated and recovery

    def ini(self,graph):
        self.id_list = list(graph.nodes)
        self.load = graph


