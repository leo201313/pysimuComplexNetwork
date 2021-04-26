import networkx as nx
import pynetsimu.MixNetwork as pns
import json
import numpy as np
import warnings

warnings.filterwarnings("ignore")
####################################################
dataset = 'facebook_combined'

data_addr = "../data/" + dataset + ".txt"
pos_addr = "../data/" + dataset + ".json"
####################################################
# ATTACK_METHOD = 'Recalculated Degree'
ATTACK_METHOD = 'RANDOM'

####################################################

if __name__ == '__main__':
    net = pns.MixNetwork()
    net.ini(data_addr,ATTACK_METHOD)
    max_step = 1000

    scentence = "- Network initiate completes.\n" + '- '+ net.describe_overall() + '\n'
    print(scentence)

    while net.step < max_step:
        net.one_step()
        if (net.step % 5 == 0):
            num, rate, waste_load = net.describe_defeated_breif()
            sentence0 = '- Breifly Description in Step ' + str(net.step) + '.\n' + \
                       'Defeated nodes number is: ' + str(num) + '. Rate is: ' + str(rate) + \
                       '. Total wasted load is: ' + str(waste_load) + '.\n'
            print(sentence0)

        if (net.step % 100 == 0):
            largest_components_num, rate = net.describe_defeated_normal()
            sentence1 = '- Normal Description in Step ' + str(net.step) + '.\n' + \
                       ' Largest components nodes number: ' + str(
                largest_components_num) + '. Connectivity rate is: ' + str(rate) + '.\n'
            print(sentence1)

        end_flag, end_type = net.whether_end()
        if end_flag:
            if end_type == 1:
                print("- Power run out end!")
            elif end_type == 2:
                print("- Over attack capacity end!")

            num, rate, waste_load = net.describe_defeated_breif()
            sentence0 = '- Breifly Description in Step ' + str(net.step) + '.\n' + \
                        'Defeated nodes number is: ' + str(num) + '. Rate is: ' + str(rate) + \
                        '. Total wasted load is: ' + str(waste_load) + '.\n'
            print(sentence0)

            break










