from math import lcm

# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Dictionary of modules. Data is formatted thus:
# key = module name
# value = [ type, [dest1, dest2, dest2], state | stored_values{} ]
# type = the char indicating what type of module this is
# state = True or False for on or off - used by flip-flop(%) modules
# stored_values = dictionary of values where key is input module and value is a value - used by conjuction(&) modules
modules = {}

# Import all modules
for line in input:
    fullname, dests = line.split(" -> ")
    if fullname == "broadcaster":
        name = fullname
    else:
        name = fullname[1:]
    modules[name] = [fullname[0]]
    modules[name].append([a.strip() for a in dests.split(", ")])
    if fullname[0] == "%":
        modules[name].append(False)

# Initialize all conjunction modules to find inputs and set stored values for each to low
for name, module_data in modules.items():
    if module_data[0] == "&":
        stored_values_list = {}
        for compare_name, compare_module_data in modules.items():
            if name in compare_module_data[1]:
                stored_values_list[compare_name] = False        # False means low
        modules[name].append(stored_values_list)

# Press the button. Start the machine!
def push_the_button():
    global high_pulses, low_pulses

    retval = ""

    this_tick_queue = [("broadcaster", False, "button")]
    next_tick_queue = []
    while True:
        # Take an pulse off this queue
        (dest, high_or_low, sender) = this_tick_queue.pop(0)

        # Catch output modules that aren't listed in modules
        if dest in modules:
            this_module = modules[dest]

            # If this module is a broadcaster then just broadcast this high_or_low to all module destinations
            if this_module[0] == "b":
                for module_dest in this_module[1]:
                    next_tick_queue.append((module_dest, high_or_low, dest))
            
            # If this module is a flip-flop..
            elif this_module[0] == "%":
                # If the pulse is low then flip the state and send a pulse
                if high_or_low == False:
                    this_module[2] = not this_module[2]
                    for module_dest in this_module[1]:
                        next_tick_queue.append((module_dest, this_module[2], dest))
            
            # If this module is a conjunction..
            elif this_module[0] == "&":
                this_module[2][sender] = high_or_low
                # If all remembered pulses are high..
                if all([v for v in this_module[2].values()]):
                    if dest in interesting_conjunctions:
                        retval += dest
                    for module_dest in this_module[1]:
                        next_tick_queue.append((module_dest, False, dest))
                else:
                    for module_dest in this_module[1]:
                        next_tick_queue.append((module_dest, True, dest))

        # If this queue is empty then swap queues
        if this_tick_queue == []:
            # If both queues are empty then stop processing
            if next_tick_queue == []:
                break
            else:
                this_tick_queue = next_tick_queue
                next_tick_queue = []

    # This retval method fails if two interesting conjunctions fire at the same time. 
    # I don't care. They don't in any reasonable time. We have a solution long before that happens.
    return retval

# From reverse engineering the input I have determined that the conjunctions must all fire together are these.
# If I can find the periodicity of these 4 then a simple LCM of these 4 numbers gives us our answer. I DO NOT LIKE that 
# this puzzle required me to reverse engineer the input. I like puzzles that rely on clever coding. I saw hints that there
# were 4 cycles I needed to be interested in. Logic dictated that it must be conjunctions that would be the concentrators of
# activity and analysis of my input led me to these 4 conjunctions.
interesting_conjunctions = ['jx', 'tn', 'vc', 'hd']

# Iterate until we've found the period of all 4 interesting_conjunctions
periods = []
i = 0
while len(periods) < 4:
    i += 1
    retval = push_the_button()
    if retval in interesting_conjunctions:
        periods.append(i)

# Print the results
print(f"LCM: {lcm(*periods)}")