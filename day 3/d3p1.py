# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# The total of all the part numbers - the solution to this puzzle
total = 0

# Making the massive assumption that all lines are the same length.
# This saves me doing millions of len(input[y]) calls later.
max_x = len(input[0])
max_y = len(input)

# Iterate the whole grid of chars looking for where numbers start and end.
found_number = False
start_x = 0
number_positions = []
for y in range(max_y):
    for x in range(max_x):
        # We're looking for digits. What we do when we do or don't find one depends on 
        # whether we're in the middle of a number.
        if input[y][x] in ("0","1","2","3","4","5","6","7","8","9"):
            if not found_number:
                found_number = True
                start_x, start_y = x, y
        else:
            if found_number:
                found_number = False
                number_positions.append((input[y][start_x:x], start_x, x-1, y))

    # Don't let numbers wrap around from one row to the next. So if we finish a row we 
    # also finish any number we're currently processing.
    if found_number:
        found_number = False
        number_positions.append((input[y][start_x:], start_x, x, y))
    
# Iterate the list of number positions and grab all the surrounding characters
# If any of those are not "." then this is a part number
for number_pos in number_positions:
    (number, start_x, end_x, y) = number_pos

    # Grab all the surrounding characters around the number
    surrounding_chars = ""
    if y > 0:
        surrounding_chars +=  input[y-1][max(0, start_x-1):min(max_x, end_x+2)]
    if start_x > 0:
        surrounding_chars += input[y][start_x-1]
    if end_x+1 < max_x:
        surrounding_chars += input[y][end_x+1]
    if y+1 < max_y:
        surrounding_chars += input[y+1][max(0, start_x-1):min(max_x, end_x+2)]

    # Remove all the "." chars. If there's anything left then this is a part number
    surrounding_chars = surrounding_chars.replace(".", "")

    if len(surrounding_chars) > 0:
        total += int(number)

# Print the result
print(total)