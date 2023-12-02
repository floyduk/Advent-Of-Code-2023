# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

maximums = {
    "red": 12,
    "green": 13,
    "blue": 14
}

total = 0

# Process the pulls for 1 game. This is a function because I want to break out
# of BOTH loops in this function if I find a game that fails the test. I can 
# do that be returning from the function.
def process_game(pulls):
    global maximums

    for pull in pulls:
        # Break the pull into groups of cube colour and cube count
        groups = pull.split(",")

        for group in groups:
            # Get the colour and count for this group
            (group_count, group_colour) = group.strip().split(" ")

            # If this group exceeds the maximum then this whole game fails
            if int(group_count) > maximums[group_colour]:
                return False
            
    # If we get here then nothing failed and we return success
    return True

# Each line of the input is a game. Iterate the lines.
for line in input:
    # First pull out the game number.
    (game_text, pulls_text) = line.split(":")
    (blah, game_number) = game_text.split(" ")
    pulls = pulls_text.strip().split(";")

    # Start of processing a game. If process_game returns True then the game passed
    # the test and we add its game number to the total
    if process_game(pulls):
        total += int(game_number)

# Print the result
print(f"Total: {total}")