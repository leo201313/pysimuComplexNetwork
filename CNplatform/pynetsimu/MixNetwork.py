import networkx as nx
from .Nodes import Node
from .Attacker import Attacker
import random

random.seed(2021)

def relu(a):
    if a>=0:
        return a
    else:
        return 0

def maxlimit(a,limit):
    if a > limit:
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
        self.attack_method = 'RD'
        self.end_flag = False

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
        self.end_flag = False
        self.influenced = set()


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
                                order_degree_amount += (self.live_degree(nei_id) + 1)

            degree_amounts[order] = order_degree_amount
            order += 1

        live_adjacent = []
        for adj_node in adjacent:
            if self.node.state[adj_node] == 1:
                live_adjacent.append(adj_node)



        for adj in live_adjacent:
            self.influenced.add(adj)
            adj_order = adjacent[adj]
            temp_append_load = int(load_order_amounts[adj_order] * (self.live_degree(adj) + 1) / degree_amounts[adj_order])
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
            self.influenced.add(adj)
            adj_order = adjacent[adj]
            temp_append_load = int(load_order_amounts[adj_order] * self.live_degree(adj) / degree_amounts[adj_order])
            self.node.append_load[adj] = relu(self.node.append_load[adj] - temp_append_load)



    def ban_node_attack(self,nodeid):
        self.influenced.add(nodeid)
        self.node.state[nodeid] = 0
        self.redistribute(nodeid)

    def ban_node_overload(self,nodeid):
        self.influenced.add(nodeid)
        self.node.state[nodeid] = 2
        self.redistribute(nodeid)

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

    def attack(self):
        if self.attack_method == 'RD':
            concerned_nodes = self.live_nodes_in_view(self.attacker.position,self.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = self.live_degree(nodeid)
            attack_nodeid = max(degree_lst,key=degree_lst.get)
            attack_power = self.node.attack_cost[attack_nodeid] + 50
            self.attacker.consist_list[attack_nodeid] = self.node.recovery_ability[attack_nodeid]
        return attack_nodeid,attack_power

    def next_position(self,attackednode):
        if self.attack_method == 'RD':
            next_position = None
            max_degree = 0
            for randnode in self.influenced:
                if self.node.state[randnode] == 1:
                    temp_live_degree = self.live_degree(randnode)
                    if  temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree

            if next_position == None:
                print('Error: No node to be chosen as next position!')

            return next_position





        if self.attack_method == 'RANDOM':
            concerned_nodes = self.nodes_in_view(attackednode,1)
            next_position = None
            live_nodes = []
            for node in concerned_nodes:
                if self.node.state[node] == 1:
                    live_nodes.append(node)

            len_live_nodes = len(live_nodes)

            if len_live_nodes == 0:
                for randnode in self.influenced:
                    if self.node.state[randnode] == 1:
                        next_position = randnode
                        break

            else:
                randindex = random.randint(0,len_live_nodes-1)
                next_position = live_nodes[randindex]


            if next_position == None:
                print('Error: No node to be chosen as next position!')

            return next_position

    def describe_overall(self):
        sentence = 'Total nodes: ' + str(len(self.node.id_list)) + \
                   ', Total edges: ' + str(self.edge.number_of_edges()) + \
                   ', Attack Method: ' + self.attack_method
        return sentence









    def attack_update(self,iterations=5):
        iteration = 1
        while iteration <= iterations:
            early_out = 1
            temp_influenced = self.influenced.copy()
            for node in temp_influenced:
                if self.node.state[node] == 1:
                    if (self.node.load[node] + self.node.append_load[node]) > self.node.load_capacity[node]:
                        self.node.state[node] = 2
                        self.redistribute(node)
                        early_out = 0
            if early_out:
                break
            iteration += 1

    def recovery_update(self,iterations=5):
        iteration = 1
        while iteration <= iterations:
            early_out = 1
            temp_influenced = self.influenced.copy()
            for node in temp_influenced:
                if self.node.state[node] == 2:
                    if (self.node.load[node] + self.node.append_load[node]) <= self.node.load_capacity[node]:
                        self.node.state[node] = 1
                        self.reallocate(node)
                        early_out = 0
            if early_out:
                break
            iteration += 1


    def one_step(self):

        if self.attacker.power_amount < 0:
            self.end_flag = True

        if self.end_flag:
            print('Warning: Run out of Power!')
            pass

        for consist_node in self.attacker.consist_list:
            self.attacker.power_amount -= self.attacker.consist_list[consist_node]

        for node in self.influenced:
            if node in self.attacker.consist_list:
                temp_health = self.node.health[node] + relu(self.node.recovery_ability[node] - self.attacker.consist_list[node])
                self.node.health[node] = maxlimit(temp_health,100)
            else:
                temp_health = self.node.health[node] + self.node.recovery_ability[node]
                self.node.health[node] = maxlimit(temp_health, 100)


            if self.node.state[node] == 0:
                if self.node.health[node] > 50:
                    if (self.node.load[node] + self.node.append_load[node]) <= self.node.load_capacity[node]:
                        self.node.state[node] = 1
                        self.reallocate(node)
                    else:
                        self.node.state[node] = 2

        self.recovery_update()

        attack_nodeid, attack_power = self.attack()
        self.attacker.power_amount -= attack_power
        self.node.health[attack_nodeid] = self.node.health[attack_nodeid] + self.node.attack_cost[attack_nodeid] - attack_power
        self.node.state[attack_nodeid] = 0
        self.redistribute(attack_nodeid)
        self.attack_update()
        self.attacker.position = self.next_position(attack_nodeid)

    def describe_defeated_num(self):
        num = 0
        for node in self.influenced:
            if self.node.state[node] != 1:
                num += 1

        rate = num / self.node.num
        return num,rate
























