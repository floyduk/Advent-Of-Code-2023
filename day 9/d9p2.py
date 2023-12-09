# open and read the input file into a list of lists of integers
sequences = [[int(n) for n in line.split()] for line in open("input.txt", "r").read().split("\n")]

# Return the prev value in the sequence. Uses recursion
def find_prev_value(s):
    return s[0] - (0 if all(v == 0 for v in s) else find_prev_value([s[i] - s[i-1] for i in range(1, len(s))]))

# Iterate the list of sequences using find_prev_value() to find the next value. Add those values together and print it
print(f"Total: {sum([find_prev_value(sequence) for sequence in sequences])}")








# Just to explain the code above: find_prev_values is basically this:
#
# def find_prev_value(sequence):
#     if(all(v == 0 for v in sequence)):
#         # If all values in sequence are 0 then the previous value is 0
#         return 0
#     else:       
#         # Return our first sequence number - the previous value in the list
#         new_sequence = [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]
#         return sequence[0] - find_prev_value(new_sequence)
#
# For find_next_value we just add to the last value in the sequence instead of subtracting from the first
# 
#       [s[i] - s[i-1] for i in range(1, len(s))]
# Takes a sequence "s" and uses a list comprehension to return the differences between the values
# 
#       all(v == 0 for v in s)
# Returns true if all values v in sequence s are equal to 0

