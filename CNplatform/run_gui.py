import networkx as nx
import pynetsimu.MixNetwork as pns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import json
import numpy as np
import warnings
import tkinter

warnings.filterwarnings("ignore")


#########################

dataset = 'USpowerGrid'
# dataset = 'ba500'
# dataset = 'facebook_combined'

data_addr = "../data/" + dataset + ".txt"
pos_addr = "../data/" + dataset + ".json"
##########################
# ATTACK_METHOD = 'RD' #Recalculated Degree
# ATTACK_METHOD = 'RANDOM'
# ATTACK_METHOD = 'RDRS' #Recalculated Degree and Recovery Stifle
# ATTACK_METHOD = 'RANDOMRS' #Random and and Recovery Stifle
# ATTACK_METHOD = 'NND' #Neighbor Nodes of Max Degree Node
ATTACK_METHOD = 'NNDRS' #Neighbor Nodes of Max Degree Node and Recovery Stifle
##########################

if __name__ == '__main__':
    net = pns.MixNetwork()
    net.ini(data_addr,ATTACK_METHOD)

    with open(pos_addr) as f_obj:
        pos = json.load(f_obj)
        ps = {}
        for nodeid,ps_ele in pos.items():
            ps[int(nodeid)] = np.array(ps_ele)

    fig = Figure(figsize=(12, 6), dpi=100)
    ax = fig.add_subplot(111)


    def update_fig(fig,ax):
        ax.clear()
        color_map = {
            1: '#7cf4e5',  # light blue
            2: '#127fed',  # blue
            0: '#e94f49'  # red
        }
        node_colors = [color_map.get(net.node.state[node], '#53f982') for node in net.node.id_list]
        edge_colors = []
        for edge in net.edge.edges():
            if (net.node.state[edge[0]] == 1) & (net.node.state[edge[1]] == 1):
                colour = '#C0FF3E'
            else:
                colour = '#FFE4E1'

            edge_colors.append(colour)

        nx.draw(net.edge, ps, with_labels=False, node_color=node_colors, edge_color=edge_colors, node_size=10, ax=ax)
        if net.last_attacked != None:
            ax.plot(ps[net.last_attacked][0],ps[net.last_attacked][1],color='m',marker='o',markersize=5) ## purple



    mixnet = tkinter.Tk()
    mixnet.title("MixNetwork GUI")

    canvas = FigureCanvasTkAgg(fig, master=mixnet)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP,
                                fill=tkinter.BOTH,
                                expand=tkinter.YES)

    toolbar = NavigationToolbar2Tk(canvas, mixnet)
    toolbar.update()
    canvas._tkcanvas.pack(side=tkinter.TOP,
                          fill=tkinter.BOTH,
                          expand=tkinter.YES)

    text = tkinter.Text(mixnet, width=100, height=9)

    scroll = tkinter.Scrollbar()
    text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    scroll.pack(side=tkinter.LEFT, fill=tkinter.Y)

    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)


    text.insert("insert", "- Welcome to Leo Cao's MixNetwork!\n")

    def _next_step():
        net.one_step()
        update_fig(fig, ax)
        canvas.draw()
        text.insert("insert", "- One step completes.\n")
        text.insert("insert", "Step " + str(net.step) +
                    ". Last attacked node id: "+str(net.last_attacked)+
                    ". Left attack power amount: "+str(net.attacker.power_amount)+'.\n')
        text.see('insert')

    def _briefly_describe():
        num, rate, waste_load = net.describe_defeated_breif()
        sentence = '- Breifly Description in Step ' + str(net.step) + '.\n' + \
                   'Defeated nodes number is: ' + str(num) + '. Rate is: ' + str(rate) + \
                   '. Total wasted load is: ' + str(waste_load) + '.\n'
        text.insert('insert',sentence)
        text.see('insert')

    def _normal_describe():
        largest_components_num,rate = net.describe_defeated_normal()
        sentence = '- Normal Description in Step ' + str(net.step) + '.\n' + \
                   ' Largest components nodes number: ' + str(largest_components_num) + '. Connectivity rate is: ' + str(rate) + '.\n'
        text.insert('insert',sentence)
        text.see('insert')







    button0 = tkinter.Button(master=mixnet, text='Next Step', command = _next_step,height=2)
    button0.pack(side=tkinter.TOP,fill=tkinter.X)
    button1 = tkinter.Button(master=mixnet, text='Breif Description', command = _briefly_describe,height=2)
    button1.pack(side=tkinter.TOP,fill=tkinter.X)
    button2 = tkinter.Button(master=mixnet, text='Normal Description', command = _normal_describe,height=2)
    button2.pack(side=tkinter.TOP,fill=tkinter.X)

    update_fig(fig, ax)
    text.insert("insert", "- Network initiate completes.\n")
    text.insert("insert",'- '+ net.describe_overall() + '\n')




    mixnet.mainloop()























