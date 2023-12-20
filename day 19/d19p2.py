# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Dictionary of the workflows
workflows = {}
total_combinations = 0
params = "xmas"

# Walk the complete tree noting all the rules we have to match or NOT MATCH to get to an A
def process_workflow2(workflow, ranges):
    global total_combinations

    # If we arrive at an A or an R then we stop here. If it's an A then calculate the combinations and add that to the total
    if workflow == 'A' or workflow == 'R':
        if workflow == 'A':
            total_combinations += (ranges[0][1] - ranges[0][0] + 1) \
                                * (ranges[1][1] - ranges[1][0] + 1) \
                                * (ranges[2][1] - ranges[2][0] + 1) \
                                * (ranges[3][1] - ranges[3][0] + 1)
        return

    # Now loop through all the rules. For each one that is < or > we split our ranges and recurse both options
    for rule in workflows[workflow]:
        if rule[1] == '':
            process_workflow2(rule[3], ranges)
        else:
            # Making copies of lists that change so that we don't accidentally change something that affects a recursion level above
            new_ranges = list(ranges)
            new_range1 = list(ranges[params.index(rule[0])])
            new_range2 = list(ranges[params.index(rule[0])])

            # new_range1 is the range we'll pass to one side of the recurtion. new_range2 is passed to the other side by updating
            # ranges. Essentially our ranges HERE reduce in size each time we fail a condition. 
            if rule[1] == '<':
                new_range1[1] = rule[2] - 1
                new_ranges[params.index(rule[0])] = new_range1

                new_range2[0] = rule[2]
                ranges[params.index(rule[0])] = new_range2
            else:
                new_range1[0] = rule[2] + 1
                new_ranges[params.index(rule[0])] = new_range1

                new_range2[1] = rule[2]
                ranges[params.index(rule[0])] = new_range2

            process_workflow2(rule[3], new_ranges)

##########################
# PROCESSING STARTS HERE #
##########################

# Process the input file first populating the workflows dictionary and then processing the parts
for line in input:
    # Finding a blank line ends importing workflows
    if line == "": 
        workflows_complete = True
        break
    
    # Importing rules
    # Pull the line apart and create the dictionary entry as an empty list to start with        
    index_of_bracket = line.index("{")
    workflow_name = line[:index_of_bracket]
    workflow_rules = [r.split(':') for r in line[index_of_bracket+1:-1].split(',')]
    workflows[workflow_name] = []

    # Iterate the rules on this line and populate the workflows value with a list of rules
    for rule in workflow_rules:
        if len(rule) == 1:
            # This is a no-condition rule:
            workflows[workflow_name].append(('','',0,rule[0]))
        else:
            # This is a rule with a condition
            parameter, comparator, value = rule[0][0], rule[0][1], int(rule[0][2:])
            workflows[workflow_name].append((parameter,comparator,value,rule[1]))

# Walk the complete workflow tree starting with the full ranges (1-4000) for all values. Each decision point splits the ranges
# so given s<1351 one path takes s<1351 and the other takes s>=1351. Once we find an A then we stop and calculate how many
# combinations this leaf accounts for. Each decision point is mutually exclusive each way so leaves MUST be non-overlapping. 
# Credit to Darren Oakey for this insight which saved me a LOT of difficult overlap finding code.
process_workflow2("in", [[1, 4000], [1, 4000], [1, 4000], [1, 4000]])

# Print the result
print(f"Total Combinations: {total_combinations}")