import networkx as nx
from .Nodes import Node
from .Attacker import Attacker

class MixNetwork(object):
    def __init__(self):
        self.edge = nx.Graph()
        self.node = Node()
        self.attacker = Attacker()
        self.step = 0

    def ini_net(self,data_addr):
        self.edge = nx.read_edgelist(data_addr, create_using = nx.Graph(), nodetype=int)







