from math import inf
from heapq import heappop, heappush

# open and read the input file into a list of strings
input = [[int(n) for n in list(line)] for line in open("input.txt", "r").read().split("\n")]
max_y, max_x = len(input), len(input[0])

# If you're going north then your options are east, west or north again
available_directions = {
    'n': ['e', 'w'],
    's': ['e', 'w'],
    'e': ['s', 'n'],
    'w': ['s', 'n'],
    None: ['e', 's']
}

# These are the coordinate change values for each direction
dxdy = {
    'n': (0, -1),
    's': (0, 1),
    'e': (1, 0),
    'w': (-1, 0),
}

# Return true if the coordinates are in-bounds
def is_in_bounds(x, y):
    global max_x, max_y
    return 0 <= x < max_x and 0 <= y < max_y

# Return a list of edges from this node to adjascent nodes and their costs
def costs(state):
    pos, dir, count = state
    (x, y) = pos

    possible_edges = []

    # Try straight ahead
    if dir != None:
        nx = x + dxdy[dir][0]
        ny = y + dxdy[dir][1]
        if is_in_bounds(nx, ny) and count+1 <= 3:
            possible_edges.append((input[ny][nx], ((nx,ny), dir, count+1))) 

    # Try a turn
    for nd in available_directions[dir]:
        nx = x + dxdy[nd][0]
        ny = y + dxdy[nd][1]
        if is_in_bounds(nx, ny):
            possible_edges.append((input[ny][nx], ((nx,ny), nd, 1)))

    return possible_edges

# This is a pretty standard dijykstra. The costs() function is where the special cases are handled.
def find_shortest_path(start):
    frontier = [(0,  start)]
    distances = {start : 0}

    # Keep searching as long as there are nodes still in our frontier list
    while len(frontier) > 0:
        distance, state = heappop(frontier)
        pos, dir, count = state
        
        # Trap-door exit if we've reaches our target node. First solution to reach it must be the
        # fastest because we order our candidate nodes by cost
        if pos[0] == max_x-1 and pos[1] == max_y-1:
            return distance

        # Having chosen a node get a list of edges and calculate the cost to each destination node
        for (cost, edge_state) in costs(state):
            # If the calculated cost is less than the previously known cost then update
            if distance + cost < distances.get(edge_state, inf):
                distances[edge_state] = distance + cost
                heappush(frontier, (distance + cost, edge_state))

start = (0,0), None, 0
print(f"Minimum cost: {find_shortest_path(start)}")