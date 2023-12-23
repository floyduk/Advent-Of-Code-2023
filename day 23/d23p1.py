# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")
max_x, max_y = len(input[0]), len(input)
start = (input[0].index("."), 0)
end = (input[max_y-1].index("."), max_y-1)

slopes = {'>':(1,0), '<':(-1,0), 'v':(0,1), '^':(0,-1)}

# This is our graph. Nodes are keys. Values are dictionaries where keys are destination nodes and values are costs.
nodes = {
    start: {},
    end: {}
}

# True if the location is in bounds
def is_in_bounds(loc):
    return 0 <= loc[0] < max_x and 0 <= loc[1] < max_y

# Return the coordinates of a location modified by dxdy
def coord_add(loc, dxdy):
    return (loc[0] + dxdy[0], loc[1] + dxdy[1])

# Return true if the indicated location is a flat path (.)
def coord_is_flat_path(loc):
    return input[loc[1]][loc[0]] == "."

# Return a list of exits from this location excluding the direction we arrived from
def exits_from_location(loc):
    retval = []

    # If this is flat ground then search all directions    
    if coord_is_flat_path(loc):
        for dxdy in slopes.values():
            try_loc = coord_add(loc, dxdy)
            # If it's in bounds and there's no forest there then this is a valid direction to try travelling in
            if is_in_bounds(try_loc) and input[try_loc[1]][try_loc[0]] != "#":
                retval.append(try_loc)

    # If this is not flat ground then search only in the direction of the slope
    else:
        try_loc = coord_add(loc, slopes[input[loc[1]][loc[0]]])
        if is_in_bounds(try_loc) and input[try_loc[1]][try_loc[0]] != "#":
            retval.append(try_loc)

    return retval

# This function starts on a node and searches in the direction indicated until it finds another node. 
# Then it finds all the possible directiosn from there and recurses for each one.
def build_graph(this_node, next_step, nodes_travelled):
    # Make my own copy of the nodes travelled so that we don't get very confused
    my_nodes_travelled = list(nodes_travelled)
    my_nodes_travelled.append(this_node)

    # Map out this edge
    steps_on_this_edge = [this_node]
    bidirectional = True
    while True:
        here=next_step
        next_step = None
        next_locations = exits_from_location(here)

        if not coord_is_flat_path(here):
            bidirectional = False

        if len(next_locations) > 2:
            # This is a node
            if here not in nodes:
                nodes[nl] = {}

            nodes[this_node][here] = len(steps_on_this_edge)
            if bidirectional:
                nodes[here][this_node] = len(steps_on_this_edge)

            for nl in next_locations:
                build_graph(here, nl, my_nodes_travelled)
            return
        else:
            # This is a corridor or a dead end
            for nl in next_locations:
                if nl != steps_on_this_edge[-1]:
                    next_step = nl

            if next_step == None:
                # This is a dead end. Have we reached the end node?
                if here in nodes:
                    # We reached another node that we already know about
                    nodes[this_node][here] = len(steps_on_this_edge)
                    if bidirectional:
                        nodes[here][this_node] = len(steps_on_this_edge)

                return
        
        steps_on_this_edge.append(here)

longest_path = 0
def find_longest_path(here, nodes_travelled, distance):
    global longest_path

    # Make my own copy of the nodes travelled so that we don't get very confused
    my_nodes_travelled = list(nodes_travelled)
    my_nodes_travelled.append(here)

    for next_node in nodes[here].keys():
        if next_node not in my_nodes_travelled:
            if next_node == end:
                print(f"Path: {distance+nodes[here][next_node]} - {my_nodes_travelled}: ")
                longest_path = max(distance+nodes[here][next_node], longest_path)
                return
            else:
                find_longest_path(next_node, my_nodes_travelled, distance+nodes[here][next_node])

build_graph(start, coord_add(start, (0,1)), [])
find_longest_path(start, [], 0)
print(nodes)
print(f"Longest path: {longest_path}")
