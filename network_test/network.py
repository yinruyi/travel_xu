import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
G.add_edges_from([("1","2"),("1","3"),("1","4"),("1","5"),("4","5"),("4","6"),("5","6")])
pos = nx.spring_layout(G)
 
#colors = [1,2,2,2,3,1]
#nx.draw_networkx_nodes(G,pos,node_color=colors)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
 
plt.axis('off')
plt.savefig("color_nodes.png")
plt.show()