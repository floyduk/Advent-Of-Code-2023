import re
from functools import cache

# open and read the input file into a list of strings
inputdata = open("input.txt", "r").read().split("\n")

# Remove simple groups at the either end of the map in order to reduce the search space of our recursive function
def simplify_map_and_groups(map, groups):
    something_worked = True
    while something_worked and len(groups) > 0:
        something_worked = False

        # Try the first number in groups
        new_map = re.sub(r"^\.*"+('\#' * groups[0])+"[\.\?]\.*", "", map)
        if len(new_map) < len(map):
            something_worked = True
            # if(map[groups[0]]) == "?"
            groups.pop(0)
            map = new_map

        if len(groups) > 0:
            # Try the last number in groups
            new_map = re.sub(r"\.*[\.\?]"+('\#' * groups[-1])+"\.*$", "", map)
            if len(new_map) < len(map):
                something_worked = True
                groups.pop()
                map = new_map

    return[map, groups]

# Ran out of time for today and after I reached the 5+ hours on this one problem mark I started to look around for help in reddit.
# This recursive algorithm comes from https://github.com/AllanTaylor314/AdventOfCode/blob/main/2023/12.py. It's a very different
# approach than mine. Instead of looking at the spaces it steps through the map string a char at a time, looks at the leftmost 
# char and then recurses (differently depending on the char) to count the variations for the rest of the map. The absolute KEY
# to this approach is functools.cache which caches return values from this function and looks them up if future calls are made with
# the same parameters. It's not an elegant solution - it uses a lot of RAM. But it sure as hell speeds things up.
@cache
def num_valid_combos(map, groups, current_group_length = 0):
    if not map:
        # Catch the case where the last char of the map satisfies the last number in groups. This was a match
        if ((len(groups)==1 and groups[0] == current_group_length)
        or (len(groups)==0 and current_group_length == 0)):
            return 1
        
        # We've run out of map before we ran out of groups. No match here
        return 0

    c = map[0]
    map = map[1:]

    # this little dance is required because functools.cache needs parameters that can be hashed
    group, *new_groups = groups or [0]
    new_groups = tuple(new_groups)  

    # How we calculate the number of variations from here depends on what this char is
    if c == '?':
        # Count variations based on this ? being either a . or a #
        return num_valid_combos('#'+map, groups, current_group_length) + num_valid_combos('.'+map, groups, current_group_length)
    elif c == '#':
        # current_group_length is the length of the group we've found. If it's bigger than the group we're working on
        # then give up and return 0 (no matches here). Otherwise keep going with growing this current_group_length
        if current_group_length > group:
            return 0
        else:
            return num_valid_combos(map, groups, current_group_length + 1)
    elif c == '.':
        # If this is a . and we're not currently in a group then just move on. If we're in a group and this group is the right
        # length of the group we're working on then this . just ended the group - happy days. We just found a group! Otherwise,
        # this . ended our current group but the current group wasn't big enough so no match here (return 0).
        if current_group_length == 0:
            return num_valid_combos(map, groups, 0)
        if current_group_length == group:
            return num_valid_combos(map, new_groups, 0)
        return 0

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

# Part 2: Expand out the input data so everyting is 5 times bigger
for i, [map, groups] in enumerate(input):
    print(input[i])
    input[i] = ["?".join([map]*5), groups*5]
    print(input[i])

# Remove simple groups at the ends of the maps
for i, [map, groups] in enumerate(input):
    input[i] = simplify_map_and_groups(map, groups)

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
    #get_solutions(map, tuple(groups), tuple(spaces), space_left)

    total += num_valid_combos(map, tuple(groups))

# Print the result
print(f"Total working solutions: {total}")