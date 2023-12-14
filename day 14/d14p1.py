# open and read the input file into a list of strings
map = [[*line] for line in open("input.txt", "r").read().split("\n")]

max_x, max_y = len(map[0]), len(map)
total_load = 0

# Tilt platform. Make all round boulders roll north
for y in range(max_y):
    for x in range(max_x):
        # Loop through all the chars in the map looking for boulders
        if map[y][x] == 'O':
            # And when we find one move it north until it hits the edge or something else
            by = y
            while by > 0 and map[by-1][x] == '.':
                map[by-1][x] = 'O'
                map[by][x] = '.'
                by -= 1

            # This is the boulder's final location. May as well total the load now.
            total_load += max_y - by

# Print the restul
print(f"Total: {total_load}")