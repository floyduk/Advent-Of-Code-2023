import networkx as nx

# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Use networkx Graphs with Stoer Wagner function
G = nx.Graph()

for line in input:
    nodes = line.replace(":", "").split()

    for node in nodes:
        if nodes[0] != node:
            G.add_edge(nodes[0], node)

cv, p= nx.stoer_wagner(G)
print(len(p[0])*len(p[1]))