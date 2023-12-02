# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# process the pulls for 1 game
def process_game(pulls):
    # This is where we keep our list of observed minimums
    minimums = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for pull in pulls:
        # Get the group of cubes for 1 game
        groups = pull.split(",")

        # Process each group and if a group has more of a colour than we've seen before
        # then update our minimums dict
        for group in groups:
            (group_count, group_colour) = group.strip().split(" ")

            if int(group_count) > minimums[group_colour]:
                minimums[group_colour] = int(group_count)

    # Calculate the power of this game by multiplying the minimums
    retval = 1
    for k in minimums.keys():
        retval *= minimums[k]

    # Return it
    return retval

# Each line of the input is a game. Iterate the lines.
total = 0
for line in input:
    # First pull out the game number then ignore it because we don't need it in part 2
    (game_text, pulls_text) = line.split(":")
    pulls = pulls_text.strip().split(";")

    # Start of processing a game
    total += process_game(pulls)

# Print the result
print(f"Total: {total}")