import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
from random import randrange
from ast import literal_eval as le

USERID = 230377912

def gen_rand_graph(G,id_counter,conn_counter):
    for i in range(0, id_counter):
        G.add_node(i)

    for c in range(0,conn_counter):
        G.add_edge(randrange(0, id_counter), randrange(0, id_counter))
    pass


def parsegraph(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        lines = fp.read().splitlines()
    pass
    kek = le(lines[0])
    return kek

lol = parsegraph(str(USERID)+"_graphdata.txt")
print(lol[1][0])
graphedges = []
for link in lol[0]:
    a = link["from"]
    b = link["to"]
    graphedges.append([a, b])


print(graphedges)

G = nx.from_edgelist(graphedges)

# G = nx.Graph()

labels = []
nx.set_node_attributes(G, labels, 'labels')

for node in G:
    for ent in lol[1]:
        if node == ent["id"]:
            print(node)
            G.nodes[node]['labels'] = ent['label']
    # print(node)
    # print("lel")
    # print(lol[1][1])
    # node['labels']=lol[1][node]['label']
    # print(lol[1])
    # print(node["id"])

# G = nx.k_core(G, k=2)

#G = nx.karate_club_graph()
#G = nx.random_powerlaw_tree(50, gamma=4, seed=None, tries=10000)
#G = nx.k_core(G, k=2)


cliq = list(nx.algorithms.community.k_clique_communities(G, 4))
print(cliq)
# todel = []
# for c in cliq:
#     if USERID in c:
#         print(c)
#     else:
#         todel.append(c)
#         pass
# for d in todel:
#     print("deleted "+str(d))
#     G.remove_nodes_from(d)



#nbrs = nx.all_neighbors(G, str(USERID))
# color_map=[]
# for node in G:
#     print(node)
#     color_map[int(node)]="red"

# nx.draw(G, node_color=color_map, with_labels=True)
nx.write_gexf(G, str(USERID)+"test.gexf")
nx.draw(G, with_labels=True)
#
plt.show()