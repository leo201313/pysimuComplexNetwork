import networkx as nx
from .Nodes import Node
from .Attacker import Attacker
import random
from math import sqrt

random.seed(2021)

def relu(a):
    if a>=0:
        return a
    else:
        return 0

def maxlimit(a,limit):
    if a < 0:
        return 0
    elif a > limit:
        return limit
    else:
        return a



class MixNetwork(object):
    def __init__(self):
        self.edge = nx.Graph()
        self.node = Node()
        self.attacker = Attacker()
        self.influenced = set()
        self.step = 0
        self.attack_method = 'Recalculated Degree'
        self.end_flag = False
        self.last_attacked = None
        self.origin_max_components_num = None

    def ini(self,data_addr,attack_method='Recalculated Degree'):
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
        self.attacker.ini(attack_method=attack_method)
        self.end_flag = False
        self.influenced = set()
        self.attack_method = attack_method
        self.last_attacked = None
        self.step = 0
        self.origin_max_components_num = None


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
        adjacent = {}
        degree_amounts = {}
        adjacent[nodeid] = 0
        order = 1
        load_amout = self.node.load[nodeid]
        load_order_amounts = {}

        self.influenced.add(nodeid)

        while order <= max_order:
            if order == max_order:
                temp_load_amount = load_amout
            else:
                temp_load_amount = int(load_amout * attenuation)
                load_amout -= temp_load_amount

            load_order_amounts[order] = temp_load_amount
            order_degree_amount = 0
            temp_adjacent = adjacent.copy()

            for temp_node in temp_adjacent:
                if adjacent[temp_node] == (order-1):
                    neighbors = list(self.edge.neighbors(temp_node))
                    for nei_id in neighbors:
                        if nei_id not in adjacent:
                            adjacent[nei_id] = order
                            if self.node.state[nei_id] == 1:
                                order_degree_amount += self.live_degree(nei_id)

            degree_amounts[order] = order_degree_amount
            order += 1

        live_adjacent = []
        for adj_node in adjacent:
            if self.node.state[adj_node] == 1:
                live_adjacent.append(adj_node)

        for adj in live_adjacent:
            adj_order = adjacent[adj]
            if degree_amounts[adj_order] != 0:
                self.influenced.add(adj)
                temp_append_load = int(load_order_amounts[adj_order] * self.live_degree(adj) / degree_amounts[adj_order])
                self.node.append_load[adj] += temp_append_load

    def reallocate(self,nodeid,max_order=2,attenuation=0.6):
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

            temp_adjacent = adjacent.copy()
            for temp_node in temp_adjacent:
                if adjacent[temp_node] == (order-1):
                    neighbors = list(self.edge.neighbors(temp_node))
                    for nei_id in neighbors:
                        if nei_id not in adjacent:
                            adjacent[nei_id] = order
                            order_degree_amount += self.live_degree(nei_id)

            degree_amounts[order] = order_degree_amount
            order += 1

        adjacent.pop(nodeid)
        self.influenced.add(nodeid)

        for adj in adjacent:
            adj_order = adjacent[adj]
            if degree_amounts[adj_order] != 0:
                self.influenced.add(adj)
                temp_append_load = int(load_order_amounts[adj_order] * self.live_degree(adj) / degree_amounts[adj_order])
                self.node.append_load[adj] = relu(self.node.append_load[adj] - temp_append_load)



    # def ban_node_attack(self,nodeid):
    #     self.influenced.add(nodeid)
    #     self.node.state[nodeid] = 0
    #     self.redistribute(nodeid)
    #
    # def ban_node_overload(self,nodeid):
    #     self.influenced.add(nodeid)
    #     self.node.state[nodeid] = 2
    #     self.redistribute(nodeid)

    def live_nodes_in_view(self,nodeid,view_range):
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

        if self.node.state[nodeid] != 1:
            nodes_viewed.pop(0)

        return nodes_viewed

    def nodes_in_view(self,nodeid,view_range):
        nodes_viewed = []
        temp_viewed = []
        nodes_viewed.append(nodeid)
        temp_viewed.append(nodeid)
        vieworder = 1
        while vieworder <= view_range:
            next_temp_viewed = []
            for temp_node in temp_viewed:
                neighbors = list(self.edge.neighbors(temp_node))
                for nei in neighbors:
                    if nei not in nodes_viewed:
                        nodes_viewed.append(nei)
                        next_temp_viewed.append(nei)
            temp_viewed = next_temp_viewed
            vieworder += 1
        return nodes_viewed



    def describe_overall(self):
        sentence = 'Total nodes: ' + str(len(self.node.id_list)) + \
                   ', Total edges: ' + str(self.edge.number_of_edges()) + \
                   ', Attack Method: ' + self.attack_method
        return sentence

    def compute_recovery(self,nodeid):
        # now_recovery = int(sqrt(self.node.recovery_ability[nodeid]*self.node.health[nodeid]) + 5)
        now_recovery = int(sqrt(self.node.recovery_ability[nodeid]) *
                           (self.node.health[nodeid]) * (self.node.health[nodeid] + 10) / 100 + 5)
        return now_recovery




    def attack_update(self,iterations=5):
        iteration = 1
        while iteration <= iterations:
            early_out = 1
            temp_influenced = self.influenced.copy()
            for node in temp_influenced:
                if self.node.state[node] == 1:
                    if (self.node.load[node] + self.node.append_load[node]) > self.node.load_capacity[node]:
                        self.node.state[node] = 2
                        self.node.health[node] = 0
                        self.redistribute(node)
                        early_out = 0
            if early_out:
                break
            iteration += 1




    def one_step(self):
        for consist_node in self.attacker.consist_list:
            self.attacker.power_amount -= self.attacker.consist_list[consist_node]

        consume = 0
        for node in self.influenced.copy():
            if self.node.health[node] != 100:
                if node in self.attacker.consist_list:
                    consume += self.attacker.consist_list[node]
                    temp_health = self.node.health[node] + relu(self.compute_recovery(node) - self.attacker.consist_list[node])
                    self.node.health[node] = maxlimit(temp_health,100)
                else:
                    temp_health = self.node.health[node] + self.compute_recovery(node)
                    self.node.health[node] = maxlimit(temp_health, 100)

            if (self.node.health[node] > 50) & (self.node.state[node]!=1) :
                self.node.state[node] = 1
                self.node.append_load[node] = 0
                self.reallocate(node)

        attack_nodeid, attack_power = self.attacker.attack(self)
        consume += attack_power
        self.attacker.last_consume = consume
        self.redistribute(attack_nodeid)
        self.attack_update()
        self.last_attacked = attack_nodeid
        self.attacker.position = self.attacker.next_position(self)


        self.step += 1



    def whether_end(self):
        end_type = 0
        if self.attacker.power_amount < 0:
            self.end_flag = True
            end_type = 1
        if self.attacker.last_consume > self.attacker.max_attack_capacity:
            self.end_flag = True
            end_type = 2
        return self.end_flag,end_type



    def describe_defeated_breif(self):
        num = 0
        waste_load = 0
        for node in self.influenced:
            if self.node.state[node] != 1:
                num += 1
                waste_load += self.node.load[node]

        rate = num / self.node.num
        return num,rate,waste_load

    def live_graph(self):
        live = []
        for nodeid in self.node.id_list:
            if self.node.state[nodeid] == 1:
                live.append(nodeid)
        liveG= self.edge.subgraph(live)
        return liveG

    def describe_defeated_normal(self):
        if self.origin_max_components_num == None:
            origin_largest_components = max(nx.connected_components(self.edge), key=len)
            self.origin_max_components_num = len(origin_largest_components)
        lg = self.live_graph()
        largest_components = max(nx.connected_components(lg), key=len)
        largest_components_num = len(largest_components)
        rate = largest_components_num / self.origin_max_components_num
        return largest_components_num,rate




























