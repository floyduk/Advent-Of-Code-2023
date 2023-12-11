# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

max_x, max_y = len(input[0]), len(input)
columns_galaxy_count = [0 for n in range(max_x)]
rows_galaxy_count = [0 for n in range(max_y)]
galaxies = []

# Iterate the map finding the galaxies and counting galaxies in each row and column
for y in range(max_y):
    for x in range(max_x):
        if input[y][x] == "#":
            galaxies.append([x, y])
            columns_galaxy_count[x] += 1
            rows_galaxy_count[y] += 1

galaxy_count = len(galaxies)

# Calculate the remap value for each row and column based on rows/cols with no galaxies
# So at the end of this we have 2 lists where the list index is the starting value and the
# list value is the mapped value. One list for x values and one list for y values. So to remap
# a location you do new_x = col_map[old_x]
row_map = []
count_blank_rows = 0
for y in range(max_y):
    row_map.append(y + count_blank_rows)
    if rows_galaxy_count[y] == 0:
        count_blank_rows += 1
    
col_map = []
count_blank_cols = 0
for x in range(max_x):
    col_map.append(x + count_blank_cols)
    if columns_galaxy_count[x] == 0:
        count_blank_cols += 1

# Remap the galaxy locations based on galaxy expansion - make a new list of galaxy locations
# Using the remap data we just made
remapped_galaxies = [[col_map[galaxies[i][0]], row_map[galaxies[i][1]]] for i in range(galaxy_count)]

# Find all permutations of galaxy pairs and calculate the manhattan distance between them. Keep a running total.
total = 0
for gal1 in range(galaxy_count-1):
    for gal2 in range(gal1+1, galaxy_count):
        [g1x, g1y], [g2x, g2y] = remapped_galaxies[gal1], remapped_galaxies[gal2]
        total += abs(g1x - g2x) + abs(g1y - g2y)

# Print the total
print(f"Total distance: {total}")