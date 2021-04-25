class Attacker(object):
    def __init__(self):
        self.position = None
        self.view_range = 2
        self.power_amount = 0
        self.max_attack_capacity = 0
        self.consist_list = {} ## list for consist attacking

    def ini(self,position=1,poweramount = 10000,max_attack_capacity=1000,view_range=2):
        self.position = position
        self.power_amount = poweramount
        self.max_attack_capacity = max_attack_capacity
        self.view_range = view_range
        self.consist_list = {}


