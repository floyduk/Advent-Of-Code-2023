# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# Keep a list of the count of each card. Initialize it with 1 for every input line
card_count = []
for i in range(len(input)):
    card_count.append(1)


for i in range(len(input)):
    # Get the line from input
    line = input[i]

    # Split it down into the stuff we need
    card_name, part2 = line.split(":")
    part1, part2 = part2.split("|")
    winning_numbers = part1.strip().split()
    my_numbers = part2.strip().split()

    # Get the intersection of winning numbers and our numbers
    intersection = [num for num in winning_numbers if num in my_numbers]
    matches = len(intersection)

    # If we have matches then add more copies of subsequent cards
    if matches > 0:
        print(f"{card_name}: {len(intersection)} matches.")
        for j in range(matches):
            card_count[i+j+1] += card_count[i]
            print(f"Won {card_count[i]} more copies of card number {i+j+2}")
    else: 
        print(f"{card_name}: {len(intersection)} matches.")

# Print the total number of cards we have
print(sum(card_count))