# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

map = []

# Doesn't actually rotate the map. It actually inverts it along the diagonal from top left to bottom right
# But that doesn't matter for this puzzle. We long as x becomes y we're happy.
def rotate_map(map):
    new_map = ["".join([line[i] for line in map]) for i in range(len(map[0]))]
    return new_map

# Searches down to find a pair of rows that match and then outwards from there to check if it's a mirror line
def find_horizontal_mirror(map):
    for i in range(len(map)-1):
        if map[i] == map[i+1]:
            if sum([1 for j in range(0, min(i+1, len(map)-1-i)) if map[i-j] != map[i+1+j]]) == 0:
                # All rows above and below match out to the closest edge
                return i + 1
            
    # Return 0 if no mirror row found
    return 0

##########################
# Processing starts here #
##########################

# Iterate the input dealing with one map at a time until we're done
total = 0
for line in input:
    if line == "":
        # This is the end of a map - process it now
        # For simplicity sake I added a blank line at the end of the input files so that we don't miss the last map
        print("\n".join(map))
        horizontal_mirror_pos = find_horizontal_mirror(map)
        print(f"Horizontal: {horizontal_mirror_pos}")
        total += horizontal_mirror_pos * 100
        if horizontal_mirror_pos == 0:
            vertical_mirror_pos = find_horizontal_mirror(rotate_map(map))
            print(f"Vertical: {vertical_mirror_pos}")
            total += vertical_mirror_pos

        # Clear map ready for the next one
        map = []
    else:
        # This is a map line - add it to the current map
        map.append(line)

# Print the total
print(f"Total: {total}")