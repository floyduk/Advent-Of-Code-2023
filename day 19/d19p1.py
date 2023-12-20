# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Dictionary of the workflows and the total needed for part 1
workflows = {}
total = 0

# This function returns either A or R by following workflow rules recursively all the way down until we get one an A or R
def process_workflow(workflow, part):
    if workflow == 'A' or workflow == 'R':
        return workflow

    for rule in workflows[workflow]:
        if rule[1] == '':
            return process_workflow(rule[3], part)
        elif rule[1] == '>':
            if part[rule[0]] > rule[2]:
                return process_workflow(rule[3], part)
        elif rule[1] == '<':
            if part[rule[0]] < rule[2]:
                return process_workflow(rule[3], part)

# Process the input file first populating the workflows dictionary and then processing the parts
workflows_complete = False
for line in input:
    # Finding a blank line triggers the change from importing workflows to processing parts
    if line == "": 
        workflows_complete = True
        continue
    
    # Importing rules
    if not workflows_complete: 
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
    
    # Processing parts
    else:
        # Pull the line apart until we have a dictionary of x:xval, m:mval etc
        part = {p[0]: int(p[2:]) for p in line[1:-1].split(',')}

        # Call our recursive function which returns A or R. If we get an A then sum the part values
        if(process_workflow("in", part) == "A"):
            total += sum(part.values())

# Print the result
print(f"Total: {total}")
