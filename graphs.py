import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
from random import randrange
import copy

# def gen_rand_user(G,id):
#     G.add_node(id)
#     pass




def gen_rand_graph(G,id_counter,conn_counter):
    for i in range(0, id_counter):
        G.add_node(i)

    for c in range(0,conn_counter):
        G.add_edge(randrange(0, id_counter), randrange(0, id_counter))
    pass


# G = nx.karate_club_graph()
G = nx.random_powerlaw_tree(100, gamma=3, seed=None, tries=5000)


#G = nx.Graph()
# remove = [node for node,degree in dict(G.degree()).items() if degree > 2]
# https://stackoverflow.com/questions/18261587/python-networkx-remove-nodes-and-edges-with-some-condition
#gen_rand_graph(G, 25, 25)
# G = nx.petersen_graph()

cliq = list(nx.algorithms.community.k_clique_communities(G, 4))
print(cliq)
# берем всех 1соседей нулевого
first_neighbors = []
second_neighbors = []
#
#
#
#
# useful_nodes = []
#
#
# print(str(first_neighbors))
# # X = G.copy(as_view=False)
# nodelist = copy.deepcopy(G.nodes())
# for node in nodelist:
#     if G.degree[node] < 2:
#         G.remove_node(node)

sets = [list(x) for x in cliq]


color_map=[]
for node in G:
    color_map.append('blue')

first_neighbors.append(0)
first_neighbors.extend(nx.neighbors(G,0))
for n in first_neighbors:
    color_map[n]='red'
#
# for s in second_neighbors:
#     #color_map.append('blue')
#     print("second "+str(s))
#     useful_nodes.extend(nx.neighbors(G, s))
#
# useful_nodes = list(dict.fromkeys(useful_nodes))
# print(useful_nodes)
#
# nodelist2 = copy.deepcopy(G.nodes())
# print(nodelist2)
# for node in nodelist2:
#     if node not in useful_nodes:
#         print(str(node in useful_nodes))
#         print("removing "+str(node))
#         G.remove_node(node)
#
# cl = list(nx.find_cliques(G))
# print(cl)
#

#
# print(color_map)
# X = G.copy(as_view=False)
#
for clique in sets:
    print(clique)
    if 0 not in clique:
        print("removed cliques " + str(clique))
        # G.remove_nodes_from(clique)
    else:
        for i in clique:
            color_map[i] = 'green'

nx.draw(G, node_color=color_map, with_labels=True)
# nx.draw(X, with_labels=True)
# nx.draw(G, node_color=color_map, with_labels=True)
plt.show()