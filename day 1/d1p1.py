# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

total = 0

# Look at me, all bright eyed and enthusastic in part one, using a list comprehension and feeling
# all smug about it.. right before part 2 is going to kick my ass and turn a DAY 1 challenge into 
# a hair pulling ordeal. 
# So yeah, list comprehension to pull out everything except digits.. could have been a regex..
# And then just grab the first and last char in the remaining string to get the answer.
for line in input:
    numbers_only = [x for x in line if x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]
    number = numbers_only[0] + numbers_only[-1]
    total += int(number)
    print(f"line: {line} numbers_only: {numbers_only} number:{number}")

print(f"Total: {total}")