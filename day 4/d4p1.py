# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# The total at the end
total = 0

# Iterate the list of cards splitting out the data then getting the intersection of the two lists and calculating 
# the score based on the number of matches
for line in input:
    # Split the line down into the stuff we need
    card_name, part2 = line.split(":")
    part1, part2 = part2.split("|")
    winning_numbers = part1.strip().split()
    my_numbers = part2.strip().split()

    # Get the intersection of winning numbers and our numbers
    intersection = [num for num in winning_numbers if num in my_numbers]
    matches = len(intersection)

    # If there is more than one matching number then add to our total score
    if matches > 0:
        total += pow(2, matches-1)

# Print the result
print(total)