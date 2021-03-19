import networkx as nx
import pynetsimu.MixNetwork as pns
#########################
data_addr = "../data/USpowerGrid.txt"

if __name__ == '__main__':
    net = pns.MixNetwork()
    net.ini(data_addr)




