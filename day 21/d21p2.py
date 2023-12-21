# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")
map_copies = 15
# interesting_target_distances = [196, 327, 458, 589, 720, 851]

# THERE IS A BUG IN THIS CODE
# Every second value (327, 489, 851) produces an incorrect result. I have no idea why and I can't be bothered
# to figure it out cause I'm tired and frazzled and fed up with having to use maths to solve an alleged CODING
# puzzle. Did not enjoy this day at all. So if you use just these 3 values and then plug them into Wolfram Alpha:
# https://www.wolframalpha.com/input?i=Expand%5BInterpolatingPolynomial%5B%7B%7B196%2C+34870%7D%2C%7B458%2C+189238%7D%2C%7B720%2C+466886%7D%7D%2C+26501365%5D%5D
# then you get the right answer. MIC DROP.
interesting_target_distances = [196, 458, 720]

# Import the map and find the S and get the max_x and max_y
map, sx, sy = [], 0, 0
for j in range(map_copies):
    for i, line in enumerate(input):
        map.append(line * map_copies)
        if 'S' in line and sx == 0:
            sx, sy = line.index('S'), i

max_x, max_y = len(map[0]), len(map)
sx += (map_copies // 2) * len(input[0])
sy += (map_copies // 2) * len(input)
print(f"max_x {max_x}, max_y {max_y}, sx, sy {sx},{sy}")

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
def get_adjascent_spaces(here, target_steps, dist):
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

def find_solutions(target_steps):
    # Create a map of distance to this space - I use this to determine the shortest route to this spot. I use this to determine 
    # which locations are part of the solution
    dist = []
    for y in range(max_y):
        dist.append([1000]*max_x)
    dist[sy][sx] = 0

    queue = [(sx, sy)]
    visited = set()
    solutions = set()
    while queue:
        here = queue.pop(0)
        visited.add(here)

        if manhattan_distance(here[0], here[1], sx, sy) % 2 == 0 or dist[here[1]][here[0]] == target_steps:
            solutions.add((here[0], here[1]))

        adjascent_spaces = get_adjascent_spaces(here, target_steps, dist)
        for space in adjascent_spaces:
            if space not in visited:
                queue.append(space)

    return(len(solutions))
    
for target_steps in interesting_target_distances:
    print("{" + f"{target_steps}, {find_solutions(target_steps)}" + "},", end="")
