# open and read the input file into a list of strings
input = open("sample.txt", "r").read().split("\n")

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
def search_in_direction(x, y, d):
    count = 0
    if d == "u":    # up
        for search_y in range(y, -1, -1):
            if [x, search_y] in tunnel_coords and input[search_y][x] in "-LFJ7":
                count += 1
    elif d == "d":    # down
        for search_y in range(y, max_y, 1):
            if [x, search_y] in tunnel_coords and input[search_y][x] in "-LFJ7":
                count += 1
    elif d == "l":    # left
        for search_x in range(x, -1, -1):
            # if x == 14 and y == 3:
            #     print(f"{search_x}, {y}: input[y][search_x]")
            if [search_x, y] in tunnel_coords and input[y][search_x] in "|LFJ7":
                count += 1
    elif d == "r":    # right
        for search_x in range(x, max_x, 1):
            if [search_x, y] in tunnel_coords and input[y][search_x] in "|LFJ7":
                count += 1

    # if [x, y] in [[14, 3], [7, 4], [8, 4], [9, 4], [7, 5], [8, 5], [6, 6], [14, 6]]:
    #     print(f"Direction: {d}, Count: {count}")

    return count

# Go through every location on the map searching in all 4 directions and counting 
# how many pipes cross the path to the edge - note cross, not follow. If there is
# an even number then this space is outside. An odd number means inside. Ignore 
# locations that are part of the tunnel.
for y in range(max_y):
    for x in range(max_x):
        if [x, y] not in tunnel_coords:
            uc = search_in_direction(x, y, "u")
            dc = search_in_direction(x, y, "d")
            lc = search_in_direction(x, y, "l")
            rc = search_in_direction(x, y, "r")
            total_crosses = uc + dc + lc + rc
            if total_crosses % 2 == 1:
                inside_spaces.append([x, y])

print(inside_spaces)
print(f"Number of inside spaces: {len(inside_spaces)}")

# wrong_answers = set(inside_spaces) - set([[14, 3], [7, 4], [8, 4], [9, 4], [7, 5], [8, 5], [6, 6], [14, 6]])
# print(f"{wrong_answers}")

print(f"TESTING INSIDE")
for [x, y] in [[14, 3], [7, 4], [8, 4], [9, 4], [7, 5], [8, 5], [6, 6], [14, 6]]:
    if [x, y] in tunnel_coords:
        print(f"\n{x}, {y} is in tunnel coords")
    else:
        uc = search_in_direction(x, y, "u")
        dc = search_in_direction(x, y, "d")
        lc = search_in_direction(x, y, "l")
        rc = search_in_direction(x, y, "r")
        total_crosses = uc + dc + lc + rc
        num_odd = 1 if uc % 2 != 0 else 0
        num_odd += 1 if dc % 2 != 0 else 0
        num_odd += 1 if lc % 2 != 0 else 0
        num_odd += 1 if rc % 2 != 0 else 0
    print(f"{x}, {y}\t{uc}\t{dc}\t{lc}\t{rc}\tTotal crosses: {total_crosses} Num_odd: {num_odd}")

print(f"TESTING OUTSIDE")
# [[0, 0], [0, 1], [0, 2], [3, 2], [4, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [9, 8]]
for [x, y] in [[3, 2], [4, 4], [9, 8]]:
    if [x, y] in tunnel_coords:
        print(f"\n{x}, {y} is in tunnel coords")
    else:
        uc = search_in_direction(x, y, "u")
        dc = search_in_direction(x, y, "d")
        lc = search_in_direction(x, y, "l")
        rc = search_in_direction(x, y, "r")
        total_crosses = uc + dc + lc + rc
        num_odd = 1 if uc % 2 != 0 else 0
        num_odd += 1 if dc % 2 != 0 else 0
        num_odd += 1 if lc % 2 != 0 else 0
        num_odd += 1 if rc % 2 != 0 else 0
    print(f"{x}, {y}\t{uc}\t{dc}\t{lc}\t{rc}\tTotal crosses: {total_crosses} Num_odd: {num_odd}")