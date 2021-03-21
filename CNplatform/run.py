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
data_addr = "../data/USpowerGrid.txt"
pos_addr = "../data/USpowerGrid.json"
# data_addr = "../data/ba500.txt"
# pos_addr = "../data/ba500.json"
# data_addr = "../data/facebook_combined.txt"
# pos_addr = "../data/facebook_combined.json"

if __name__ == '__main__':
    net = pns.MixNetwork()
    net.ini(data_addr)

    with open(pos_addr) as f_obj:
        pos = json.load(f_obj)
        ps = {}
        for nodeid,ps_ele in pos.items():
            ps[int(nodeid)] = np.array(ps_ele)

    fig = Figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)


    def update_fig(fig,ax):
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



    button = tkinter.Button(master=mixnet, text='Next Step', command = _next_step)
    button.pack(side=tkinter.TOP,fill=tkinter.X)

    update_fig(fig, ax)
    text.insert("insert", "- Network initiate completes.\n")
    text.insert("insert",'- '+ net.describe_overall() + '\n')



    mixnet.mainloop()























