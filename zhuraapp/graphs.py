import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
from random import randrange
from ast import literal_eval as le

USERID = 32953591

def gen_rand_graph(G,id_counter,conn_counter):
    for i in range(0, id_counter):
        G.add_node(i)

    for c in range(0,conn_counter):
        G.add_edge(randrange(0, id_counter), randrange(0, id_counter))
    pass


def clear_graph_2(G):
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


def parsegraph(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        lines = fp.read().splitlines()
    pass
    kek = le(lines[0])
    return kek

def clean_graph(graphdata):
    graphedges = []
    for link in graphdata[0]:
        a = link["from"]
        b = link["to"]
        graphedges.append([a, b])

    # создаем nx-граф из данных о связях
    G = nx.from_edgelist(graphedges)

    # убираем шум
    G = nx.k_core(G, k=2)
    edgestostay = []
    nodestostay = []

    # списки оставшихся после удаления нод и связей
    for node in G:
        nodestostay.append(str(node))

    for edge in G:
        edgestostay.append(str(edge))

    # списки на удаление
    edgestoremove = []
    for edge in graphdata[0]:
        # если есть в списке, то ничего. Иначе удалить
        pass

    nodestoremove = []
    for node in graphdata[1]:
        pass

    return graphdata
    pass

lol = parsegraph(str(USERID)+"_graphdata.txt")
print(lol[1][0])
graphedges = []
for link in lol[0]:
    a = link["from"]
    b = link["to"]
    graphedges.append([a, b])


print(graphedges)

G = nx.from_edgelist(graphedges)
G = clear_graph_2(G)
nx.draw(G, with_labels=True)
G = nx.k_core(G, k=2)

plt.show()