# open and read the input file into a list of lists of integers
sequences = [[int(n) for n in line.split()] for line in open("input.txt", "r").read().split("\n")]

# Return the next value in the sequence. Uses recursion - see d9p2.py for an explanation of this
def find_next_value(s):
    return s[-1] + (0 if all(v == 0 for v in s) else find_next_value([s[i] - s[i-1] for i in range(1, len(s))]))

# Iterate the list of sequences using find_next_value() to find the next value. Add those values together and print it
print(f"Total: {sum([find_next_value(sequence) for sequence in sequences])}")