# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# Read input file and turn it into a list of pairs of time and distance values - yeah I can write stupid 
# unmaintainable code too. I try not to for the most part but once in a while it's fun.
races = [[input[0].split()[1:][i], input[1].split()[1:][i]] for i in range(len(input[0].split()[1:]))]

# Iterate the races
win_count_product = 1
for race in races:
    race_time, target_distance = int(race[0]), int(race[1])

    # Iterate the possible values in this race and track how many of them give a winning result
    win_count = 0
    for hold_button_time in range(race_time):
        # distance travelled in this race is: hold_button_time * (race_time - hold_button_time)
        if hold_button_time * (race_time - hold_button_time) > target_distance:
            win_count += 1
    
    # Keep track of the product of the win counts - this is our puzzle result
    win_count_product *= win_count

# Print the result
print(f"Win count product: {win_count_product}")