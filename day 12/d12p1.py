# open and read the input file into a list of strings
inputdata = open("input.txt", "r").read().split("\n")

# This function compares a given map against a given solution. If the solution matches the map return True.
def check_against_map(map, spaces, groups):
    # Create a string version of the solution
    solution_map = "." * spaces[0]
    for i in range(len(groups)):
        solution_map += "#" * groups[i]
        solution_map += "." * spaces[i+1]

    # Compare the string solution to the map and return true if it matches
    for [i, char] in enumerate(map):
        if char == "." or char == "#":
            if char != solution_map[i]:
                return False

    return True

# Find all possible permutations of spaces given a list of spaces and the number of spaces to add
solutions = []
def get_solutions(spaces, space_left):
    global solutions

    if space_left == 0:
        if spaces not in solutions:
            solutions.append(spaces)
        return
    
    for i in range(len(spaces)):
        new_spaces = spaces.copy()
        new_spaces[i] += 1
        get_solutions(new_spaces, space_left-1)

##########################
# PROCESSING STARTS HERE #
##########################

# Read input file and create a list of problems. The first value in the list is the map ("???.###") 
# and the second value is a list of integers (1,1,3)
input = []
for line in inputdata:
    map, numbers = line.split(" ")
    groups = [int(n) for n in numbers.split(",")]
    input.append([map, groups])

# Iterate the rows of the input. I keep 2 lists - one is the groups and one is the spaces. A solution is
# the interleaving of those, eg space[0], group[0], space[1], group[1], space[2]. So there will always be 
# one more value in spaces than in groups.
# This chunk of code calculates how many spaces we need to add in andmakes the minimum possible spaces list.
# I then use a recursive function to find all the permutations of where those spaces could be added.
# And then I test each permutation to see if it fits the given map. 
total = 0
for [map, groups] in input:
    # The amount of *wiggle room* we have 
    space_left = len(map) - sum(groups) - (len(groups) - 1)

    # Spaces is a list of the size of the gaps between the groups. At the start and end these can be 0
    # but spaces between groups must be 1 or more. A solution is spaces and groups interleaved
    spaces = [0]
    for i in range(len(groups) - 1):
        spaces.append(1)
    spaces.append(0)
    
    # Recursive function to get all the permutations of where spaces can be added
    get_solutions(spaces, space_left)

    # Count all the permutations that match the map
    for s in solutions:
        if check_against_map(map, s, groups):
            total += 1 
    solutions = []

# Print the result
print(f"Total working solutions: {total}")