# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

max_y, max_x = len(input), len(input[0])    # Limits of the input grid
sx, sy = 0,0                                # Location of S
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

# Follow the pipe path until we get back to S
[x, y] = tunnel_coords[0]
[last_x, last_y] = [sx, sy]
while [x, y] != [sx, sy]:
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

print(int(len(tunnel_coords) / 2))
