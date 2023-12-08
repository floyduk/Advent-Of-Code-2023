from math import lcm

# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# This function is cut/pasted from part 1. It returns the number of steps from the given
# start node to an end node (ends in Z).
def find_steps_to_Z(current_node):
    step = 0
    while current_node[-1] != "Z":
        direction = direction_list[step%directions_count]
        current_node = network[current_node][0 if direction == "L" else 1]
        step += 1
    return(step)

##########################
# PROCESSING STARTS HERE #
##########################

# Get the directions list from the input - line 0
direction_list = input[0]
directions_count = len(input[0]) # Used in the modulo operation later

# Build a dictionary holding the network based on the input
network = {}
for line in input[2:]:
    node_name = line.split("=")[0].strip()
    connected_nodes = line.split(",")
    network[node_name] = [connected_nodes[0][-3:], connected_nodes[1][1:4]]

# Get a list of starting nodes (nodes that end in A).
current_nodes = [n for n in network.keys() if n[-1] == "A"]

# Iterate the list of starting nodes finding how many steps each takes to get to Z
node_steps_to_Z = []
for current_node in current_nodes:
    node_steps_to_Z.append(find_steps_to_Z(current_node))

# Print the result which is the lowest common multiple of all the step counts for each path
print(f"Steps: {lcm(*node_steps_to_Z)}")