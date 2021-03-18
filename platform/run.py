import networkx as nx

#########################
data_addr = "../data/USpowerGrid.txt"

if __name__ == '__main__':
    Gf = nx.read_edgelist(data_addr, create_using = nx.Graph(), nodetype=int)
    nodes_id = list(Gf.nodes)
    print(nodes_id)
    print(Gf.degree)



