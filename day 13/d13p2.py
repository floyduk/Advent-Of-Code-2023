# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

map = []

# Return the number of chars that differ between two strings
def count_diff_chars(str1, str2):
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count

# Doesn't actually rotate the map. It actually inverts it along the diagonal from top left to bottom right
# But that doesn't matter for this puzzle. We long as x becomes y we're happy.
def rotate_map(map):
    new_map = ["".join([line[i] for line in map]) for i in range(len(map[0]))]
    return new_map

# Searches down and then outward for each row counting differences. Return if we find a position that has only 1 defect.
def find_horizontal_mirror(map):
    for i in range(len(map)-1):
        differences = 0
        print(f"Range is {i+1} {len(map)-1-i} : {min(i+1, len(map)-1-i)}")
        for j in range(0, min(i+1, len(map)-1-i)):
            print(f"row {i-j+1} vs row {i+1+j+1}: map[{i}-{j}] = {map[i-j]} vs map[{i}+1+{j}] = {map[i+1+j]}")
            differences += count_diff_chars(map[i-j],map[i+1+j])

        # if sum([1 for j in range(0, min(i, len(map)-1-i)) if map[i-j] != map[i+1+j]]) == 0:
            # All rows above and below match out to the closest edge
        if differences == 1:
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