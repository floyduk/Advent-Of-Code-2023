# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

max_y, max_x = len(input), len(input[0])    # Limits of the input grid
sx, sy = 0,0                                # Location of S
tunnel_coords = []                          # The list of tunnel segments connected to S
inside_spaces = []                          # The list of spaces inside the tunnel loop

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

# Follow the pipe path until we get back to S filling in tunnel_coords as we go
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

# Search from x, y in a direction to the edge. Return the number of crossing pipes that are in the tunnel_coords list.
def clear_in_direction(x, y, d):
    if d == "u":    # up
        if y == 0:
            return True
        for search_y in range(y, -1, -1):
            if [x, search_y] in tunnel_coords and input[search_y][x] in "|-LFJ7":
                return False
    elif d == "d":    # down
        if y == max_y-1:
            return True
        for search_y in range(y, max_y, 1):
            if [x, search_y] in tunnel_coords and input[search_y][x] in "|-LFJ7":
                return False
    elif d == "l":    # left
        if x == 0:
            return True
        for search_x in range(x, -1, -1):
            if [search_x, y] in tunnel_coords and input[y][search_x] in "|-LFJ7":
                return False
    elif d == "r":    # right
        if x == max_x-1:
            return True
        for search_x in range(x, max_x, 1):
            if [search_x, y] in tunnel_coords and input[y][search_x] in "|-LFJ7":
                return False

    return True


inside_direction = [[" "] * max_x for y in range(max_y)]
for [x, y] in tunnel_coords:
    # print(f"{x}, {y}: {input[y][x]}")
    if input[y][x] == "-":
        if clear_in_direction(x, y, "u"):
            inside_direction[y][x] = "d"
        elif clear_in_direction(x, y, "d"):
            inside_direction[y][x] = "u"
    elif input[y][x] == "|":
        print("FOUND |")
        if clear_in_direction(x, y, "l"):
            inside_direction[y][x] = "r"
        elif clear_in_direction(x, y, "r"):
            inside_direction[y][x] = "l"
    elif input[y][x] == "L":
        if clear_in_direction(x, y, "l") or clear_in_direction(x, y, "d"):
            inside_direction[x][y] = "ur"

for y in range(max_y):
    print(f"{inside_direction[y]}")


# CORRECT INSIDE: [[14, 3], [7, 4], [8, 4], [9, 4], [7, 5], [8, 5], [6, 6], [14, 6]]
# CORRECT OUTSIDE: [[0, 0], [0, 1], [0, 2], [3, 2], [4, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [9, 8]]
