# open and read the input file into a list of strings
input = open("input.txt", "r").read().split(",")

# A function that hashes the given string
def hash(str):
    current_value = 0
    for c in str:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

box = [[] for i in range(256)]

# Process each step of the instructions
for line in input:
    print(f"Line: {line}")
    if "=" in line:
        label, focal_length = line.split("=")
        box_number = hash(label)
        matching_lenses_in_box = [i for i in range(len(box[box_number])) if box[box_number][i][0] == label]
        if len(matching_lenses_in_box) == 1:
            box[box_number][matching_lenses_in_box[0]][1] = focal_length
        elif len(matching_lenses_in_box) > 1:
            print(f"REPLACE: More than one lens in box matches label: {matching_lenses_in_box}")
            exit(-1)
        else:
            box[box_number].append([label, focal_length])
        
    elif "-" in line:
        label = line[:-1]
        box_number = hash(label)
        matching_lenses_in_box = [i for i in range(len(box[box_number])) if box[box_number][i][0] == label]
        if len(matching_lenses_in_box) == 1:
            del(box[box_number][matching_lenses_in_box[0]])
        elif len(matching_lenses_in_box) > 1:
            print(f"DELETE: More than one lens in box matches label: {matching_lenses_in_box}")
            exit(-1)

# Calculate the focussing power of all lenses
focussing_powers = []
for i, b in enumerate(box):
    for j, lens in enumerate(b):
        focussing_powers.append((i+1) * (j+1) * int(lens[1]))

# Print the total
print(sum(focussing_powers))