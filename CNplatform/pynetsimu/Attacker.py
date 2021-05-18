import random
from math import sqrt

class Attacker(object):
    def __init__(self):
        self.position = None
        self.view_range = 2
        self.power_ini = 0
        self.power_amount = 0
        self.attack_method = None
        self.last_consume = 0
        self.max_attack_capacity = 0
        self.consist_list = {} ## list for consist attacking
        self.consist_threshold = {}
        self.viewed_set = set()
        self.attack_queue = []

    def ini(self,position=1,poweramount = 10000000,max_attack_capacity=1000000,view_range=2,attack_method='RANDOM'):
        self.position = position
        self.power_amount = poweramount
        self.power_ini = poweramount
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
            attack_power = net.node.attack_cost[attack_nodeid]

        ##############################################################
        if self.attack_method == 'RANDOM':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            randindex = random.randint(0, len(concerned_nodes) - 1)
            attack_nodeid = concerned_nodes[randindex]
            attack_power = net.node.attack_cost[attack_nodeid]

        #############################################################
        if self.attack_method == 'RDRS':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = net.live_degree(nodeid)
            attack_nodeid = max(degree_lst, key=degree_lst.get)
            attack_power = net.node.attack_cost[attack_nodeid]

        ##############################################################
        if self.attack_method == 'RANDOMRS':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            randindex = random.randint(0, len(concerned_nodes) - 1)
            attack_nodeid = concerned_nodes[randindex]
            attack_power = net.node.attack_cost[attack_nodeid]

        #############################################################
        if self.attack_method == 'NND':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = net.live_degree(nodeid)
            max_degree_node = max(degree_lst, key=degree_lst.get)

            nei_nodes = net.live_nodes_in_view(max_degree_node, 1)
            nei_nodes.pop(0)
            if len(nei_nodes) == 0:
                attack_nodeid = max_degree_node
                attack_power = net.node.attack_cost[attack_nodeid]

            else:
                degree_lst0 = {}
                for nodeid0 in nei_nodes:
                    degree_lst0[nodeid0] = net.live_degree(nodeid0)
                attack_nodeid = max(degree_lst0, key=degree_lst0.get)
                attack_power = net.node.attack_cost[attack_nodeid]

        #############################################################
        if self.attack_method == 'NNDRS':
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            degree_lst = {}
            for nodeid in concerned_nodes:
                degree_lst[nodeid] = net.live_degree(nodeid)
            max_degree_node = max(degree_lst, key=degree_lst.get)

            nei_nodes = net.live_nodes_in_view(max_degree_node, 1)
            nei_nodes.pop(0)
            if len(nei_nodes) == 0:
                attack_nodeid = max_degree_node
                attack_power = net.node.attack_cost[attack_nodeid]

            else:
                degree_lst0 = {}
                for nodeid0 in nei_nodes:
                    degree_lst0[nodeid0] = net.live_degree(nodeid0)
                attack_nodeid = max(degree_lst0, key=degree_lst0.get)
                attack_power = net.node.attack_cost[attack_nodeid]

        #############################################################
        if self.attack_method == 'OC':


            casecade_range = 2
            alpha1 = 15
            alpha2 = 10
            alpha0 = 2
            beta1 = 0.6
            beta2 = 0.4
            gama = 0.1

            view_range =  net.attacker.view_range + casecade_range
            concerned_nodes = net.live_nodes_in_view(net.attacker.position, net.attacker.view_range)
            viewed_nodes = net.live_nodes_in_view(net.attacker.position, view_range)

            important_value = {}
            ref_value = {}
            max_degree = 1

            # live_betweenness_lst = net.live_betweenness(net.attacker.position,compute_range=4)

            for nodeid in concerned_nodes:
                temp_live_degree = net.live_degree(nodeid)
                if temp_live_degree > max_degree:
                    max_degree = temp_live_degree

            # for nodeid in viewed_nodes:
            #     if nodeid in live_betweenness_lst:
            #         loc_betweenness = live_betweenness_lst[nodeid]
            #     else:
            #         loc_betweenness = 0

                VI = alpha1 * net.live_degree(nodeid)/max_degree \
                      # + alpha2 * loc_betweenness
                important_value[nodeid] = VI

            for nodeid in concerned_nodes:
                neighbor1 = net.live_neighbors(nodeid)
                neighbor2 = net.live_nodes_in_view(nodeid, 2)
                temp_c1 = 0
                n1_num = 0
                temp_c2 = 0
                n2_num = 0
                for nei in neighbor2:
                    if nei not in important_value:
                        impV = 0
                    else:
                        impV = important_value[nei]

                    if nei in neighbor1:
                        temp_c1 += impV
                        n1_num += 1
                    elif nei == nodeid:
                        pass
                    else:
                        temp_c2 += impV
                        n2_num += 1

                if n1_num == 0:
                    c1 = 0
                    c2 = 0
                else:
                    c1 = temp_c1 / n1_num
                    if n2_num == 0:
                        c2 = 0
                    else:
                        c2 = temp_c2 / n2_num


                ref_value[nodeid] = important_value[nodeid] + alpha0 * (beta1 * c1 + beta2 * c2) - gama * net.node.attack_cost[nodeid]

            attack_nodeid = max(ref_value, key=ref_value.get)
            attack_power = net.node.attack_cost[attack_nodeid]















        if attack_nodeid == None:
            print('Error: No node to be chosen as attacked!')

        self.power_amount -= attack_power
        net.node.health[attack_nodeid] = 0
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
        #############################################################
        if self.attack_method == 'NND':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
        #############################################################
        if self.attack_method == 'NNDRS':
            self.consist_list[net.last_attacked] = net.compute_recovery(net.last_attacked)
            for node in net.last_overload:
                self.consist_list[node] = net.compute_recovery(node)
        #############################################################
        if self.attack_method == 'OC':
            self.consist_list = {}
            self.viewed_set.add(net.last_attacked)

            for node in net.last_overload:
                self.viewed_set.add(node)

            for ele in self.viewed_set:
                self.consist_list[ele] = net.predict_recovery(ele)





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
        if self.attack_method == 'NND':
            max_degree = 0
            for randnode in net.influenced:
                if net.node.state[randnode] == 1:
                    temp_live_degree = net.live_degree(randnode)
                    if temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree
        #################################################################
        if self.attack_method == 'NNDRS':
            max_degree = 0
            for randnode in net.influenced:
                if net.node.state[randnode] == 1:
                    temp_live_degree = net.live_degree(randnode)
                    if temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree
        #################################################################
        if self.attack_method == 'OC':
            max_degree = 0
            for randnode in net.influenced:
                if net.node.state[randnode] == 1:
                    temp_live_degree = net.live_degree(randnode)
                    if temp_live_degree > max_degree:
                        next_position = randnode
                        max_degree = temp_live_degree
        #################################################################
        if next_position == None:
            print('Error: No node to be chosen as next position!')
        return next_position


