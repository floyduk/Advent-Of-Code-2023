# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# Get the directions list from the input - line 0
direction_list = input[0]
directions_count = len(input[0]) # Used in the modulo operation later

# Build a dictionary holding the network based on the input - dictionary comprehension just to show off
network = {line[:3]:[line[7:10], line[12:15]] for line in input[2:]}

current_node = "AAA"
step = 0
# Now walk the network according to the L and R directions. Use while because we need to keep
# going until we reach ZZZ even if it means looping around the directions list
while current_node != "ZZZ":
    # Use modulo to rotate around the directions list with looping at the end
    direction = direction_list[step%directions_count]

    # Move to the next node. Use ternary operation to turn L or R into 0 or 1
    current_node = network[current_node][0 if direction == "L" else 1]

    # Increment the step - this is used to count steps AND to drive the direction list modulo operation
    step += 1

# Print the result
print(f"Steps: {step}")