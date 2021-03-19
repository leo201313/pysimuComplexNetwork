import networkx as nx
from .Nodes import Node
from .Attacker import Attacker
import random

random.seed(2021)

class MixNetwork(object):
    def __init__(self):
        self.edge = nx.Graph()
        self.node = Node()
        self.attacker = Attacker()
        self.influenced = set()
        self.step = 0
        self.attack_method = 'RD'

    def ini(self,data_addr):
        """
        Initiate the MixNet
        :param data_addr: The file address of dataset
        """
        self.edge = nx.Graph()
        temp_gf = nx.read_edgelist(data_addr, create_using=nx.Graph(), nodetype=int)
        load_lst = {}
        for edge in list(temp_gf.edges):
            rand_load = random.randint(50,150)
            self.edge.add_edge(edge[0],edge[1],load=rand_load)
            if edge[0] in load_lst:
                load_lst[edge[0]] += rand_load
            else:
                load_lst[edge[0]] = rand_load

            if edge[1] in load_lst:
                load_lst[edge[1]] += rand_load
            else:
                load_lst[edge[1]] = rand_load
        self.node.ini(self.edge,load_lst)
        self.attacker.ini()
        self.influenced.add(self.attacker.position)

    def live_degree(self,nodeid):
        neighbors = list(self.edge.neighbors(nodeid))
        live_neighbors = []
        for temp_id in neighbors:
            if self.node.state[temp_id] == 1:
                live_neighbors.append(temp_id)
        return len(live_neighbors)

    def live_neighbors(self,nodeid):
        neighbors = list(self.edge.neighbors(nodeid))
        live_neighbors = []
        for temp_id in neighbors:
            if self.node.state[temp_id] == 1:
                live_neighbors.append(temp_id)
        return live_neighbors


    def redistribute(self,nodeid,max_order=2,attenuation=0.6):
        self.node.state[nodeid] = 0
        adjacent = {}
        degree_amounts = {}
        adjacent[nodeid] = 0
        order = 1
        load_amout = self.node.load[nodeid]
        load_order_amounts = {}

        while order <= max_order:
            if order == max_order:
                temp_load_amount = load_amout
            else:
                temp_load_amount = int(load_amout * attenuation)
                load_amout -= temp_load_amount

            load_order_amounts[order] = temp_load_amount
            order_degree_amount = 0

            for temp_node in adjacent:
                if adjacent[temp_node] == (order-1):
                    neighbors = self.live_neighbors(temp_node)
                    for nei_id in neighbors:
                        if nei_id not in adjacent:
                            adjacent[nei_id] = order
                            order_degree_amount += self.live_degree(nei_id)

            degree_amounts[order] = order_degree_amount
            order += 1

        adjacent.pop(nodeid)

        for adj in adjacent:
            self.influenced.add(adj)
            adj_order = adjacent[adj]
            temp_append_load = int(load_order_amounts[adj_order] * self.live_degree(adj) / degree_amounts[adj_order])
            self.node.append_load += temp_append_load

    def ban_node_attack(self,nodeid):
        self.influenced.add(nodeid)
        self.node.state[nodeid] = 0
        self.redistribute(nodeid)

    def ban_node_overload(self,nodeid):
        self.influenced.add(nodeid)
        self.node.state[nodeid] = 2
        self.redistribute(nodeid)

    def nodes_in_view(self,nodeid,view_range):
        nodes_viewed = []
        temp_viewed = []
        nodes_viewed.append(nodeid)
        temp_viewed.append(nodeid)
        vieworder = 1
        while vieworder <= view_range:
            next_temp_viewed = []
            for temp_node in temp_viewed:
                neighbors = self.live_neighbors(temp_node)
                for nei in neighbors:
                    if nei not in nodes_viewed:
                        nodes_viewed.append(nei)
                        next_temp_viewed.append(nei)
            temp_viewed = next_temp_viewed
            vieworder += 1
        return temp_viewed

    def attack(self):
        if self.attack_method == 'RD':
            concerned_nodes = self.nodes_in_view(self.attacker.position,self.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = self.live_degree(nodeid)
            attack_nodeid = max(degree_lst,key=degree_lst.get)
            attack_power = self.node.attack_cost[attack_nodeid] + 50
            self.attacker.power_amount -= attack_power
            self.attacker.consist_list[attack_nodeid] = self.node.recovery_ability[attack_nodeid]
        return attack_nodeid,attack_power

    def one_step(self):
        pass














