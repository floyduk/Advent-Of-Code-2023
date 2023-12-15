# open and read the input file into a list of strings
input = open("sample.txt", "r").read().split(",")

# A function that hashes the given string
def hash(str):
    current_value = 0
    for c in str:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

# Print total
print(sum([hash(str) for str in input]))