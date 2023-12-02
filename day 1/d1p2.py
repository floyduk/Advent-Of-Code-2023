# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

total = 0

# The list of stuff that matches a number and the number it should become
lookup_list = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9"
}

# iterate the list and work left to right looking for stuff that starts with 
# one of the lookup_list dictionary keys. There's probably some smarter way to 
# do this with a list comprehension but it's past midnight and it has been a 
# long day. This gets the job done. Good night.
for line in input:
    lineout = ""
    i = 0
    while i < len(line):
        for lookup in lookup_list:
            if line[i:].startswith(lookup):
                lineout += lookup_list[lookup]
                break
        i += 1

    total += int(lineout[0] + lineout[-1])

print(f"Total: {total}")