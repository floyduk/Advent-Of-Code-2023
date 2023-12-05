# open and read the input file
input_file = open("input.txt", "r")
input = input_file.read().split("\n")

rulesets = {}
current_ruleset = ""

def lookup_mapped_value(ruleset, val):
    global rulesets

    # Iterate the rules looking for one that applies to this value
    for rule in rulesets[ruleset]:
        [dest_start, source_start, range] = rule

        # If this rule applies to this mapping then return the mapped value
        if val >= source_start and val - source_start < range:
            return dest_start + (val - source_start)
    
    # If no rules have applied to this mapping then return the original value
    return val

for line in input:
    if line.startswith("seeds:"):
        seeds = line.split()[1:]
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

# Look through all the seeds translating to location and keep track of the lowest one
locations = []
for seed in seeds:
    soil = lookup_mapped_value("seed-to-soil", int(seed))
    fertilizer = lookup_mapped_value("soil-to-fertilizer", soil)
    water = lookup_mapped_value("fertilizer-to-water", fertilizer)
    light = lookup_mapped_value("water-to-light", water)
    temperature = lookup_mapped_value("light-to-temperature", light)
    humidity = lookup_mapped_value("temperature-to-humidity", temperature)
    location = lookup_mapped_value("humidity-to-location", humidity)

    locations.append(location)

print(F"{sorted(locations)}")
print(f"Lowest location value: {sorted(locations)[0]}")