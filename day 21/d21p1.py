# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")
target_steps = 64

# Import the map and find the S and get the max_x and max_y
map, sx, sy = [], 0, 0
for i, line in enumerate(input):
    map.append(line)
    if 'S' in line:
        sx, sy = line.index('S'), i
max_x, max_y = len(map[0]), len(map)

# Returns the manhattan distance between 2 points. This is used because only locations that are 
# even numbers of steps from start are reachable. It's a chess board. I use the result of this %2 = 0
# to count the solutions
def manhattan_distance(x1,y1,x2,y2):
    return abs(x2-x1) + abs(y2-y1)

# Return true if x, y is in bounds
def in_bounds(x, y):
    return 0 <= x < max_x and 0 <= y < max_y

# return a list of adjascent map spaces that don't contain obstructions and haven't been searched yet 
# or have but we've found a better route
def get_adjascent_spaces(here):
    (x, y) = here
    dist_to_here = dist[y][x]
    retval = []

    if dist_to_here == target_steps:
        return []

    for dxdy in [(-1,0), (1,0), (0,-1), (0,1)]:
        if in_bounds(x+dxdy[0], y+dxdy[1]) and map[y+dxdy[1]][x+dxdy[0]] != "#" and dist[y+dxdy[1]][x+dxdy[0]] > dist_to_here: 
            if dist[y+dxdy[1]][x+dxdy[0]] > dist_to_here + 1:
                retval.append((x+dxdy[0], y+dxdy[1]))
                dist[y+dxdy[1]][x+dxdy[0]] = dist_to_here + 1

    return retval

# Create a map of distance to this space - I use this to determine the shortest route to this spot. I use this to determine 
# which locations are part of the solution
dist = []
for y in range(max_y):
    dist.append([100]*max_x)
dist[sy][sx] = 0

queue = [(sx, sy)]
visited = set()
solutions = set()
while queue:
    here = queue.pop(0)
    visited.add(here)

    if manhattan_distance(here[0], here[1], sx, sy) % 2 == 0 or dist[here[1]][here[0]] == target_steps:
        solutions.add((here[0], here[1]))

    adjascent_spaces = get_adjascent_spaces(here)
    for space in adjascent_spaces:
        if space not in visited:
            queue.append(space)

# Print the solution
print(f"Possible spaces: {len(solutions)}")

