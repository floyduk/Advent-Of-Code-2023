# open and read the input file into a list of strings
map = [[*line] for line in open("input.txt", "r").read().split("\n")]

max_x, max_y = len(map[0]), len(map)
total_load = 0

# Calculate load
def calculate_load():
    total_load = 0

    for y in range(max_y):
        for x in range(max_x):
            if map[y][x] == 'O':
                total_load += max_y - y
    
    return total_load


def tilt_north():
    global map
    # Tilt platform. Make all round boulders roll north
    for y in range(max_y):
        for x in range(max_x):
            # Loop through all the chars in the map looking for boulders
            if map[y][x] == 'O':
                # And when we find one move it north until it hits the edge or something else
                by = y
                while by > 0 and map[by-1][x] == '.':
                    by -= 1
                map[y][x] = '.'
                map[by][x] = 'O'

def tilt_south():
    global map
    # Tilt platform. Make all round boulders roll north
    for y in range(max_y-1, -1, -1):
        for x in range(max_x):
            # Loop through all the chars in the map looking for boulders
            if map[y][x] == 'O':
                # And when we find one move it north until it hits the edge or something else
                by = y
                while by < max_y-1 and map[by+1][x] == '.':
                    by += 1
                map[y][x] = '.'
                map[by][x] = 'O'

def tilt_west():
    global map
    # Tilt platform. Make all round boulders roll west
    for x in range(max_x):
        for y in range(max_y):
            # Loop through all the chars in the map looking for boulders
            if map[y][x] == 'O':
                # And when we find one move it west until it hits the edge or something else
                bx = x
                while bx > 0 and map[y][bx-1] == '.':
                    bx -= 1
                map[y][x] = '.'
                map[y][bx] = 'O'

def tilt_east():
    global map
    # Tilt platform. Make all round boulders roll north
    for x in range(max_x-1, -1, -1):
        for y in range(max_y):
            # Loop through all the chars in the map looking for boulders
            if map[y][x] == 'O':
                # And when we find one move it north until it hits the edge or something else
                bx = x
                while bx < max_x-1 and map[y][bx+1] == '.':
                    bx += 1
                map[y][x] = '.'
                map[y][bx] = 'O'

# The period value here is something I figured out by printing 1000 load values out and graphing them in google sheets
period = 22
target = 1000000000
value_closest_to_target = target // period * period

# Calculate the max %period=0 value that is before our target value
print(f"Value closest to target: {value_closest_to_target}")
print(value_closest_to_target % period)

# 1000 is enough to see the periodicity, which in my case is 22
last_loop_values = []
loop_values = []
for i in range(1000):
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()
    # Once we get past the settling down phase (approx 50 cycles) we start recording load values. I know from external
    # analysis that the period of my cycle is 22 so I just keep track of 22 values and when 2 in a row match I know the
    # pattern has settled down. From there I can step forward from the closest value to the target to the target and 
    # lookup what the answer will be from the loop values
    if i > 50 and i % 22 == 0:
        if loop_values == last_loop_values:
            # Looping values have settled down. Now we can calculate the value at 1000000000
            print(last_loop_values)
            for i in range(value_closest_to_target, target):
                print(f"Cycle number: {i+1}: value from list: {last_loop_values[i-value_closest_to_target]}")
            exit()
        last_loop_values = loop_values
        loop_values = [calculate_load()]
        print(f"Iteratations: {i+1}: {calculate_load()}")
    else:
        loop_values.append(calculate_load())
