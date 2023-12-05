# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

rulesets = {}               # A dictonary of lists of ruleset ranges
seeds = []                  # A list of lists containing the seed ranges

# Possible range overlaps:
#        XXXXXX = rule range
#        XXXXXX
# |----| XXXXXX             Case 1 - no overlap
#        XXXXXX |----|      Case 2 - no overlap
# |---------|XX             Case 3 - Overlap from below
#        XX|---------|      Case 4 - Overlap from above
#        X|--|X             Case 5 - Overlap all inside
#     |----------|          Case 6 - Overlap on both sides
#        XXXXXX
#        XXXXXX

# This function detects which kind of overlap this is and updtes input and output ranges accordingly
# New input ranges are made for parts that lie outside the rule range. Output ranges are made for 
# parts that lie within the rule range
def find_overlap_type(rs, rr, s, r):
    if s < rs:                          # Start of range is below rule range
        if s+r-1 < rs:                  # End of range is below rule range
            return 1                    # Case 1
        elif rs <= s+r-1 <= rs+rr-1:    # End of range is inside rule range
            return 3                    # Case 3
        elif s+r-1 > rs+rr-1:           # End of range is above rule range
            return 6                    # Case 6
    elif rs <= s <= rs+rr-1:            # Start of range is inside rule range
        if rs <= s+r-1 <= rs+rr-1:      # End of range is inside rule range
            return 5                    # Case 5
        elif s+r-1 > rs+rr-1:           # End of range is above rule range
            return 4                    # Case 4
    elif s > rs+rr-1:                   # Start of range is above rule range
        return 2                        # Case 2

# This function maps a source range to a destination range. What it does exactly depends on which
# overlap case is found. 
def map_ranges(ruleset, ranges):
    input_ranges = ranges
    output_ranges = []

    # Iterate all the input ranges bearing in mind that our code below may add more. So we do 
    # this with pop and while instead of "for range in input_ranges"
    while input_ranges:
        [s, r] = input_ranges.pop()

        # Ignore any ranges that have 0 range
        if r != 0: 
            # First find the rule that applies to this start value
            rule_applied = False
            for rule in rulesets[ruleset]:
                [ds, ss, sr] = rule

                overlap_case = find_overlap_type(ss, sr, s, r)

                if rule_applied == False: 
                    if overlap_case == 3:                                   # Case 3
                        input_ranges.append([s, ss-s])
                        output_ranges.append([ds, r-(ss-s)])
                        rule_applied = True

                    elif overlap_case == 4:                                 # Case 4
                        output_ranges.append([ds + (s-ss), sr - (s-ss)])
                        input_ranges.append([ss+sr, r-(sr - (s-ss))])
                        rule_applied = True

                    elif overlap_case == 5:                                 # Case 5
                        output_ranges.append([ds + (s - ss), r])
                        rule_applied = True

                    elif overlap_case == 6:                                 # Case 6
                        input_ranges.append([s, ss-s])
                        output_ranges.append([ds, sr])
                        input_ranges.append([ss+sr, (s+r-1) - (ss+sr-1)])
                        rule_applied = True

                    # Fall through for case 1 & 2 - do nothing
            
            # If we've iterated all the rules and nothing got applied then just make a simple output range
            if rule_applied == False:
                output_ranges.append([s, r])

    # Return the resulting output ranges
    return output_ranges

# Import data from the input file building the rulesets and seeds. At the end of this seeds is a nice list
# of lists. The inner list is a pair consisting of start and range values. Also at the end of this the 
# rulesets dictionary contains lists of ruleset ranges in the form [dest_start, source_start, range_len]
current_ruleset = ""
for line in input:
    if line.startswith("seeds:"):
        values = line.split()[1:]
        start_range = -1
        for v in values:
            if start_range == -1:
                start_range = int(v)
            else:
                seeds.append([start_range, int(v)])
                start_range = -1

    elif line == "":
        # End of a block 
        current_ruleset = ""
    elif "map:" in line:
        # Start of a block
        current_ruleset = line.split()[0]
        rulesets[current_ruleset] = []
    else:
        numbers = line.split()
        rulesets[current_ruleset].append([int(n) for n in numbers])

# Case tests - if you set up a seed-to-soil rule of 100 10 10 and then run these tests you can check
# that all the overlap cases are working as expected
# soil = map_ranges("seed-to-soil", [[1, 5]])       # Case 1
# soil = map_ranges("seed-to-soil", [[30, 5]])      # Case 2
# soil = map_ranges("seed-to-soil", [[5, 10]])      # Case 3
# soil = map_ranges("seed-to-soil", [[15, 10]])     # Case 4
# soil = map_ranges("seed-to-soil", [[12, 5]])      # Case 5
# soil = map_ranges("seed-to-soil", [[5, 20]])      # Case 6

# Run the map ranges function on all the data ruleset by ruleset
soil = map_ranges("seed-to-soil", seeds)
fertilizer = map_ranges("soil-to-fertilizer", soil)
water = map_ranges("fertilizer-to-water", fertilizer)
light = map_ranges("water-to-light", water)
temperature = map_ranges("light-to-temperature", light)
humidity = map_ranges("temperature-to-humidity", temperature)
location = map_ranges("humidity-to-location", humidity)

# Select the range starts and then sort them and then pick the lowest one
print(f"Lowest location: {sorted([l[0] for l in location])[0]}")
