# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

dxdy = {
    '3': (0, -1),
    '1': (0, 1),
    '0': (1, 0),
    '2': (-1, 0),
}

# Return a new loc that has moved in direction dir
def move(loc, dir, dist):
    return (loc[0] + dxdy[dir][0] * dist, loc[1] + dxdy[dir][1] * dist)

# This rather trivial looking algorithm calculates the area of an irregular polygon. I found it here:
# https://www.wikihow.com/Calculate-the-Area-of-a-Polygon (scroll down to part 3)
def calculate_area(vert):
    step1 = sum([vert[i][0] * vert[i+1][1] for i in range(len(vert)-1)])
    step2 = sum([vert[i][1] * vert[i+1][0] for i in range(len(vert)-1)])
    step3 = step1 - step2
    return step3 // 2

##########################
# PROCESSING STARTS HERE #
##########################

# Follow the instructions one by one keeping a list of the locations in trench_locs
loc = (0, 0)
vertices = [(0,0)]
length_of_trench = 0
for line in input:
    # Pull the values we need out of the hex value in the input
    hexval = line.split()[2]
    dist = int(hexval[2:-2], 16)
    dir = hexval[-2]

    # Follow the given instructions noting the vertices of our trench polygon and the total length of it
    loc = move(loc, dir, dist)
    length_of_trench += dist
    vertices.append(loc)

# Calculate and print the total area
print(f"Area: {calculate_area(vertices) + (length_of_trench // 2) + 1}")