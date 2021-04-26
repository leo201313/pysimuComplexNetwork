import random
from math import sqrt

class Attacker(object):
    def __init__(self):
        self.position = None
        self.view_range = 2
        self.power_amount = 0
        self.attack_method = None
        self.last_consume = 0
        self.max_attack_capacity = 0
        self.consist_list = {} ## list for consist attacking

    def ini(self,position=1,poweramount = 10000000,max_attack_capacity=10000,view_range=2,attack_method='RANDOM'):
        self.position = position
        self.power_amount = poweramount
        self.max_attack_capacity = max_attack_capacity
        self.attack_method = attack_method
        self.view_range = view_range
        self.consist_list = {}

    def attack(self,net):
        attack_nodeid = None
        attack_power = 0
        #############################################################
        if self.attack_method == 'RD':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = net.live_degree(nodeid)
            attack_nodeid = max(degree_lst, key=degree_lst.get)
            attack_power = net.node.attack_cost[attack_nodeid] + 50

        ##############################################################
        if self.attack_method == 'RANDOM':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            randindex = random.randint(0, len(concerned_nodes) - 1)
            attack_nodeid = concerned_nodes[randindex]
            attack_power = net.node.attack_cost[attack_nodeid] + 50

        #############################################################
        if self.attack_method == 'RDRS':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = net.live_degree(nodeid)
            attack_nodeid = max(degree_lst, key=degree_lst.get)
            attack_power = net.node.attack_cost[attack_nodeid] + 50

        ##############################################################
        if self.attack_method == 'RANDOMRS':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            randindex = random.randint(0, len(concerned_nodes) - 1)
            attack_nodeid = concerned_nodes[randindex]
            attack_power = net.node.attack_cost[attack_nodeid] + 50

        #############################################################



        if attack_nodeid == None:
            print('Error: No node to be chosen as attacked!')

        self.power_amount -= attack_power
        net.node.health[attack_nodeid] = net.node.health[attack_nodeid] + net.node.attack_cost[attack_nodeid] - attack_power
        net.node.state[attack_nodeid] = 0
        return attack_nodeid, attack_power

    def update_consist(self,net):
        #############################################################
        if self.attack_method == 'RD':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
        #############################################################
        if self.attack_method == 'RANDOM':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
        #############################################################
        if self.attack_method == 'RDRS':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
            for node in net.last_overload:
                self.consist_list[node] = net.compute_recovery(node)
        #############################################################
        if self.attack_method == 'RANDOMRS':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
            for node in net.last_overload:
                self.consist_list[node] = net.compute_recovery(node)




    def next_position(self,net):
        next_position = None
        ###############################################################
        if self.attack_method == 'RD':
            max_degree = 0
            for randnode in net.influenced:
                if net.node.state[randnode] == 1:
                    temp_live_degree = net.live_degree(randnode)
                    if temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree
        #################################################################
        if self.attack_method == 'RANDOM':
            concerned_nodes = net.nodes_in_view(net.last_attacked, 1)
            live_nodes = []
            for node in concerned_nodes:
                if net.node.state[node] == 1:
                    live_nodes.append(node)

            len_live_nodes = len(live_nodes)

            if len_live_nodes == 0:
                for randnode in net.influenced:
                    if net.node.state[randnode] == 1:
                        next_position = randnode
                        break

            else:
                randindex = random.randint(0, len_live_nodes - 1)
                next_position = live_nodes[randindex]
        ##########################################################################
        if self.attack_method == 'RDRS':
            max_degree = 0
            for randnode in net.influenced:
                if net.node.state[randnode] == 1:
                    temp_live_degree = net.live_degree(randnode)
                    if temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree
        #################################################################
        if self.attack_method == 'RANDOMRS':
            concerned_nodes = net.nodes_in_view(net.last_attacked, 1)
            live_nodes = []
            for node in concerned_nodes:
                if net.node.state[node] == 1:
                    live_nodes.append(node)

            len_live_nodes = len(live_nodes)

            if len_live_nodes == 0:
                for randnode in net.influenced:
                    if net.node.state[randnode] == 1:
                        next_position = randnode
                        break

            else:
                randindex = random.randint(0, len_live_nodes - 1)
                next_position = live_nodes[randindex]
        ##########################################################################
        if next_position == None:
            print('Error: No node to be chosen as next position!')
        return next_position


