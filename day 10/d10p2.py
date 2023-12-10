# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

max_y, max_x = len(input), len(input[0])    # Limits of the input grid
sx, sy = 0, 0                                # Location of S
tunnel_coords = []                          # The list of tunnel segments connected to S

# Find coordinates of S
for y in range(max_y):
    for x in range(max_x):
        if input[y][x] == "S":
            sx, sy = x, y

# Find a starting pipe that connects to S - look in all 4 directions until we find one that links to S
if sy > 0 and input[sy-1][sx] in "|F7":
    tunnel_coords.append([sx, sy-1])
elif sy < max_y - 1 and input[sy+1][sx] in "|LJ":
    tunnel_coords.append([sx, sy+1])
elif sx > 0 and input[sy][sx-1] in "-FL":
    tunnel_coords.append([sx, sy+1])
elif sx < max_x - 1 and input[sy][sx+1] in "-7J":
    tunnel_coords.append([sx, sy+1])

# Follow the pipe path until we get back to S filling in tunnel_coords as we go. At the end of this we have 
# a list of location coords that are part of the tunnel. 
[x, y] = tunnel_coords[0]
[last_x, last_y] = [sx, sy]
while [x, y] != [sx, sy]:
    # If we know the pipe shape and the last x,y then we know where it leads
    if input[y][x] == "|":  
        if last_y == y - 1:
            [last_x, last_y, x, y] = [x, y, x, y+1]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x, y-1]
            tunnel_coords.append([x, y])
    elif input[y][x] == "-":
        if last_x == x - 1:
            [last_x, last_y, x, y] = [x, y, x+1, y]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x-1, y]
            tunnel_coords.append([x, y])
    elif input[y][x] == "L":
        if last_y == y - 1:
            [last_x, last_y, x, y] = [x, y, x+1, y]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x, y-1]
            tunnel_coords.append([x, y])
    elif input[y][x] == "J":
        if last_y == y - 1:
            [last_x, last_y, x, y] = [x, y, x-1, y]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x, y-1]
            tunnel_coords.append([x, y])
    elif input[y][x] == "7":
        if last_y == y + 1:
            [last_x, last_y, x, y] = [x, y, x-1, y]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x, y+1]
            tunnel_coords.append([x, y])
    elif input[y][x] == "F":
        if last_y == y + 1:
            [last_x, last_y, x, y] = [x, y, x+1, y]
            tunnel_coords.append([x, y])
        else: 
            [last_x, last_y, x, y] = [x, y, x, y+1]
            tunnel_coords.append([x, y])

# This function searches from a given x, y up to the top edge of the map. Along the way it counts how many times 
# the tunnel crosses our search path. The way is does this is complex due to the character based nature of the
# map. But it centres on what is or isn't a crossing. A "-" is always a crossing because it comes in on one side
# and goes out on the other. Pairs "JF" and "L7" are crossings because they go in one side and out the other.
# Everything else is just noise. We we use a lot of search/replace to simplify down our list of chars from our
# search path to leave ONLY the real crossings and if the number is odd then return true.
def is_inside(x, y):
    # Edge locations CANNOT be inside
    if y == 0 or x == 0 or y == max_y-1 or x == max_x-1:
        return False

    # Iterate out to the edge making a crossing_chars string of all the tunnel chars encountered on the way
    crossing_chars = ""
    for search_y in range(y, -1, -1):
        if [x, search_y] in tunnel_coords and input[search_y][x] in "-LFJ7":
            crossing_chars = crossing_chars + input[search_y][x]

    # Turn "JF" and "L7" into "-"" because they form a single crossing
    current_len = 0
    while(len(crossing_chars) != current_len):
        current_len = len(crossing_chars)
        crossing_chars = crossing_chars.replace("JF", "-")
        crossing_chars = crossing_chars.replace("L7", "-")

    # Remove "J7" and "LF" because they are U shaped ends that don't form a crossing
    current_len = 0
    while(len(crossing_chars) != current_len):
        current_len = len(crossing_chars)
        crossing_chars = crossing_chars.replace("J7", "")
        crossing_chars = crossing_chars.replace("LF", "")

    # If there is an odd number of crossing then we're inside
    return len(crossing_chars) % 2 == 1

# Search the entire map (skipping any spaces that are part of the tunnel) searching for locations that are inside the loop.
count_inside_locs = 0 
for y in range(max_y):
    for x in range(max_x):
        if [x, y] not in tunnel_coords and is_inside(x, y):
            count_inside_locs += 1

# Print the result
print(f"Total inside spaces: {count_inside_locs}")
