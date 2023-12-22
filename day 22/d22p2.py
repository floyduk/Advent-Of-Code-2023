import copy

# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Global variables
blocks = []
connections = {}

# Basic coordinate maths
def subtract_coordinates(start, end):
    return (end[0]-start[0], end[1]-start[1], end[2]-start[2])

def add_coordinates(coord, dxdydz):
    return (coord[0]+dxdydz[0], coord[1]+dxdydz[1], coord[2]+dxdydz[2])

def divide_coordinates(coord, divisor):
    return (coord[0] // divisor, coord[1] // divisor, coord[2] // divisor)

# This function is used in 2 ways. The basic case is - can this one block move down.
# In that case the minus_blocks list contains a single block. we make a list of coordinates 
# of all OTHER blocks and try to move each coordinate in this block down
# The second use case is where we want to see if minus_blocks[0] can move if minus_blocks[1]
# is removed. So minus_blocks contains 2 blocks, the first of which is the one we want to test
# and the second is the block we're removing.
def block_can_move_down(minus_blocks, blocks):
    # Generate a list of all coordinates of all blocks except this block
    all_coords = []
    for b in blocks:
        if b not in minus_blocks:
            all_coords += b

    # Look at each coord in this block and if the space under it is part of
    # another block or the ground then we can't move down
    for coord in minus_blocks[0]:
        down_coord = (coord[0], coord[1], coord[2]-1)
        if down_coord in all_coords or down_coord[2] == 0:
            return False
        
    return True

# Move all coords in this block down 1 (z=z-1)
def move_block_down(block):
    for i in range(len(block)):
        coord = block.pop(0)
        block.append((coord[0], coord[1], coord[2]-1))

def drop_blocks(blocks):
    blocks_that_moved = set()
    something_moved = True
    while something_moved:
        something_moved = False

        for i, b in enumerate(blocks):
            if block_can_move_down([b], blocks):
                move_block_down(b)
                something_moved = True
                blocks_that_moved.add(i)

    return len(blocks_that_moved)

##########################
# PROCESSING STARTS HERE #
##########################

# Import data, creating a list of blocks - one per line
for line in input:
    block = []

    # Get the start and end points of this block
    start,end = [tuple([int(x) for x in coord.split(",")]) for coord in line.split("~")]

    # Add the start block so it appears first
    block.append(start)

    # Get the difference between start and end, then the size of the longest dimension. We will use these toegther 
    # to give us a one-at-a-time step we can add to the start n times to generate the intermediate blocks
    diff = subtract_coordinates(start, end)
    magnitude = max([abs(x) for x in diff])

    # If there are un-made blocks in between start and end then create them and add them to block[]
    if start != end and magnitude > 1:
        step = divide_coordinates(diff, magnitude)
        intermediate_block = start
        for i in range(magnitude-1):
            intermediate_block = add_coordinates(intermediate_block, step)
            block.append(intermediate_block)

    # Add the end block so it appears last
    block.append(end)

    # Add the newly created block to the blocks list
    blocks.append(block)

# Drop all blocks that can drop - keep going until nothing moves
print(f"Dropping {len(blocks)} blocks")
drop_blocks(blocks)

# Now we're all settled we start removing blocks and seeing what moves when we do
count_blocks_that_would_move = 0
for i in range(len(blocks)):
    new_blocks = copy.deepcopy(blocks)
    new_blocks.pop(i)
    count_blocks_that_would_move += drop_blocks(new_blocks)
    print(f"{count_blocks_that_would_move}")

# Print the result
print(f"Count of blocks that would move: {count_blocks_that_would_move}")
