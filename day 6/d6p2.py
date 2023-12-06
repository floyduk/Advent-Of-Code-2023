# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

# Read input file and get the race time and distance
race_time = int(input[0].replace(" ", "").split(":")[1])
target_distance = int(input[1].replace(" ", "").split(":")[1])
print(f"Time: {race_time} Distance: {target_distance}")

# Iterate all the possible values in this race and keep track of how many win
win_count = 0
for hold_button_time in range(race_time):
    # distance travelled in this race is: hold_button_time * (race_time - hold_button_time)
    if hold_button_time * (race_time - hold_button_time) > target_distance:
        win_count += 1

# Print the result
print(f"Win count: {win_count}")