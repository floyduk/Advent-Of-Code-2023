# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# The total of all the part numbers - the solution to this puzzle
total = 0

# Making the massive assumption that all lines are the same length.
# This saves me doing millions of len(input[y]) calls later.
max_x = len(input[0])
max_y = len(input)

# Iterate the whole grid of chars looking for where numbers start and end
# and also looking for gear ("*") positions
found_number = False
start_x = 0
number_positions = []
gear_positions = []
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
        
        # If we find a * then add it to a list of gear locations
        if input[y][x] == "*":
            gear_positions.append((x, y))

    # Don't let numbers wrap around from one row to the next. So if we finish a row we 
    # also finish any number we're currently processing.
    if found_number:
        found_number = False
        number_positions.append((input[y][start_x:], start_x, x, y))
    
# Iterate the list of gears looking for ones that are in the area of 2 numbers
for gear in gear_positions:
    (gear_x, gear_y) = gear
    adjascent_numbers = []

    # Search the number positions to see if this gear is in their area
    for number_pos in number_positions:
        (number, start_x, end_x, y) = number_pos

        if start_x-1 <= gear_x <= end_x+1 and y-1 <= gear_y <= y+1:
            # Gear is within this number's area
            adjascent_numbers.append(number_pos)

    # Only add this gear ratio to the total if there are exactly 2 adjascent numbers    
    if len(adjascent_numbers) == 2:
        total += int(adjascent_numbers[0][0]) * int(adjascent_numbers[1][0])

# Print the result
print(total)