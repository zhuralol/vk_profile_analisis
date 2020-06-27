import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
from random import randrange
from ast import literal_eval as le
from networkx.readwrite import json_graph;

def gen_rand_graph(G,id_counter,conn_counter):
    for i in range(0, id_counter):
        G.add_node(i)

    for c in range(0,conn_counter):
        G.add_edge(randrange(0, id_counter), randrange(0, id_counter))
    pass


def clear_graph(G):
    l1 = len(G)
    n1 = G.number_of_edges()
    G = nx.k_core(G, k=2)
    l2 = len(G)
    n2 = G.number_of_edges()
    cliques = nx.find_cliques(G)
    cliques3 = [clq for clq in cliques if len(clq) >= 3]
    nodes = set(n for clq in cliques3 for n in clq)
    h = G.subgraph(nodes)
    deg = nx.degree(h)
    nodes = [n for n in nodes if deg[n] >= 3]
    k = h.subgraph(nodes)
    l3 = len(k)
    n3 = k.number_of_edges()
    print("1 step Number of nodes " + str(l1) + " edges " + str(n1))
    print("2 step Number of nodes " + str(l2) + " edges " + str(n2))
    print("3 step Number of nodes " + str(l3) + " edges " + str(n3))
    return k

def savegraph2(lol, G, USERDATA_PATH, userid):
    # lol - это данные о полном старом графе
    # print(lol[0][0])  {'from': 603565812, 'to': 164397292}
    # print(lol[0][1])  {'from': 603565812, 'to': 267401830}
    # print(lol[1][0]) {'id': 164397292, 'label': 'Дмитрий Сауков', 'image': 'https://sun9-31.userapi.com/c847124/v847124901/852e/gfAUypAgESo.jpg?ava=1', 'shape': 'image'}
    # print(lol[1][1]){'id': 267401830, 'label': 'Эмиль Абузяров', 'image': 'https://sun9-62.userapi.com/c856036/v856036833/ff3c7/ntY3V2Evnw4.jpg?ava=1', 'shape': 'image'}
    # G - урезанный новый граф
    oldgraph_edges = lol[0]
    oldgraph_nodes = lol[1]

    newgraph_nodes = list(G.nodes)
    # print(newgraph_nodes)
    # print(oldgraph_nodes)
    nodestodelete=[]

    newnodes_list = []
    for node in oldgraph_nodes:
        # print(node)
        for nnode in newgraph_nodes:
            # print(nnode)
            if str(node['id']) == str(nnode):
                # print(node)
                # print(node['id'])
                newnodes_list.append(node)
                pass

    # print(newnodes_list)

    newedges_list = []
    # print(oldgraph_nodes)
    newgraph_edges = G.edges()
    for edge in oldgraph_edges:
        for nedge in newgraph_edges:
            if str(edge['from']) == str(nedge[0]) and str(edge['to']) == str(nedge[1]):
                newedges_list.append(edge)
            # print(edge)
            # print(nedge)
        # print(edge)
        pass
    graph_data = [newedges_list, newnodes_list]

    with open(USERDATA_PATH + "/" + str(userid) + "/" + "graphdata.txt", 'w', encoding='utf-8') as fp:
        fp.write(str(graph_data))

def parsegraph(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        lines = fp.read().splitlines()
    pass
    kek = le(lines[0])
    return kek


def graph_main(graphdata_path, userid, USERDATA_PATH):
    lol = parsegraph(graphdata_path)

    print(lol[1][0])
    graphedges = []
    for link in lol[0]:
        a = link["from"]
        b = link["to"]
        graphedges.append([a, b])

    print(graphedges)

    G = nx.from_edgelist(graphedges)
    G = clear_graph(G)

    G = nx.k_core(G, k=2)
    savegraph2(lol, G, USERDATA_PATH, userid)
    # savegraph(G, userid, USERDATA_PATH)
    # отрисовка графа
    # nx.draw(G, with_labels=True)
    # plt.show()