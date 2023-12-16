# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")
max_y, max_x = len(input), len(input[0])

# Lookup table of what happens if a beam hits a mirror or prism depending on the direciton of the beam
interactions = {
    '.': {'n': ['n'], 's': ['s'], 'e': ['e'], 'w': ['w']},
    '/': {'n': ['e'], 's': ['w'], 'e': ['n'], 'w': ['s']},
    '\\':{'n': ['w'], 's': ['e'], 'e': ['s'], 'w': ['n']},
    '-': {'n': ['e', 'w'], 's': ['e', 'w'], 'e': ['e'], 'w': ['w']},
    '|': {'n': ['n'], 's': ['s'], 'e': ['n', 's'], 'w': ['n', 's']},
}


energized = set()           # A set of energized grid locations
beams = [[0,0,'e']]         # A list of startnig beam locations and directions
loop_detect = []            # A list of locations and directions that we've visited before

# Loop through all the beams in the list checking the grid and then moving on. We pop the beam off
# the list and then append 1 or 2 new beams onto the list as long as the new beam is in-bounds.
while beams:
    [x, y, d] = beams.pop()

    # If a beam has been at this location and travelling in this direction before then it'll do the
    # same again so don't bother doing it again. This prevents loops.
    if [x, y, d] not in loop_detect:
        loop_detect.append([x, y, d])

        # Take note that this location is energized. Note that this is a set and therefore cannot contain duplicates
        energized.add((x, y))

        # Lookup what to do whtn a beam hits this char at this direction. Calculate the new x and y (nx, ny).
        # This lookup results in a list because some chars split the beam and preoducts more than one output beam.
        for nd in interactions[input[y][x]][d]:
            nx, ny = x, y
            if nd == "n":
                ny -= 1
            elif nd == "s":
                ny += 1
            elif nd == "w":
                nx -= 1
            elif nd == "e":
                nx += 1
            
            # If this new x, y, d (nx, ny, nd) is in bounds then add this new beam
            if 0 <= nx < max_x and 0 <= ny < max_y:
                beams.append([nx, ny, nd])

# Print the result
print(len(energized))