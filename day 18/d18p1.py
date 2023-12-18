# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

dxdy = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0),
}

# Return a new loc that has moved in direction dir
def move(loc, dir):
    global dxdy
    return (loc[0] + dxdy[dir][0], loc[1] + dxdy[dir][1])

# Return the number of filled spaces once the trench has been flood filled. Or return false if flood fill goes out of bounds
def flood_fill(border_locs, start_loc):
    queue = [start_loc]
    filled_area = set([start_loc] + border_locs)    # Using a set because sets can't contain duplicates

    while queue:
        # Pop the queue and add the popped loc to the filled area
        loc = queue.pop()
        filled_area.add(loc)

        # Add new frontier locs to the queue
        for d in ['U', 'D', 'L', 'R']:
            new_loc = move(loc, d)
            if is_in_bounds(new_loc): 
                if new_loc not in filled_area:
                    queue.append(new_loc)
            else:
                return False
    
    # visualize(filled_area)

    return len(filled_area)

# Draw the map
def visualize(locs):
    for y in range(top_limit-1, bottom_limit+2):
        for x in range(left_limit-1, right_limit+2):
            if (x, y) == (0,0):
                print('#' if (x,y) in locs else '.', end="")    
            else:
                print('o' if (x,y) in locs else '.', end="")
        print("")

# We keep track of the bounds and this function returns true if a given loc is inside the bounds
top_limit, bottom_limit, left_limit, right_limit = 0, 0, 0, 0
def is_in_bounds(loc):
    return left_limit <= loc[0] <= right_limit and top_limit <= loc[1] <= bottom_limit

##########################
# PROCESSING STARTS HERE #
##########################

# Follow the instructions one by one keeping a list of the locations in trench_locs
loc = (0, 0)
trench_locs = [(0,0)]
for line in input:
    dir, dist, colour = line.split()

    for i in range(int(dist)):
        loc = move(loc, dir)
        trench_locs.append(loc)

    left_limit = min(left_limit, loc[0])
    right_limit = max(right_limit, loc[0])
    top_limit = min(top_limit, loc[1])
    bottom_limit = max(bottom_limit, loc[1])

# visualize(trench_locs)
print(f"Trench volume: {len(set(trench_locs))}")

# Flood fill
print(f"Filled volume: {flood_fill(trench_locs, (1,1))}")