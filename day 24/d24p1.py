from itertools import combinations

# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# This is the range of values that count as successes for intersection points
interesting_range = (200000000000000, 400000000000000)

# Do some basic maths to calculate the intersection of 2 lines.
# Return None if the lines are parallel or the intersection point is in the past
def get_intersection(hail1, hail2):
    x1, y1, z1, dx1, dy1, dz1 = hail1
    x2, y2, z2, dx2, dy2, dz2 = hail2

    # Calculate the slopes of the lines
    m1 = dy1/dx1
    m2 = dy2/dx2

    # Compare the slopes to determine if the paths are parallel
    if m1 == m2:
        # Same slope - parallel lines
        return None, None
    
    # Calculate a, b and c for equations ax + bx + c = 0
    c1 = (dx1 * y1 - dy1 * x1)
    c2 = (dx2 * y2 - dy2 * x2)
    b1 = -dx1
    b2 = -dx2
    a1 = dy1
    a2 = dy2

    # Use cross multiplication rule to find the intersection of two lines
    intersection_x = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
    intersection_y = (a2 * c1 - a1 * c2) / (a1 * b2 - a2 * b1)

    # Calculate what time the hailstones were at the intersection's x value
    time1 = (intersection_x - x1) / dx1
    time2 = (intersection_x - x2) / dx2

    # Times below 0 are in the past
    if time1 < 0 or time2 < 0:
        return None, None

    return (intersection_x, intersection_y)

# Import the data into a simple list of tuples (x, y, z, dx, dy, dz)
hailstones = []
for line in input:
    position, direction = line.split(" @ ")
    hailstones.append(tuple([int(a) for a in position.split(", ")] + [int(a) for a in direction.split(", ")]))

# Compare all cbombinations of hailstones 
intersection_count = 0
for hail1, hail2 in combinations(hailstones, 2):
    # Get the intersection point
    (x, y) = get_intersection(hail1, hail2)

    # If the intersection point exists and is inside the interesting_range then add 1 to our success count
    if x != None:
        if interesting_range[0] <= x <= interesting_range[1] and interesting_range[0] <= y <= interesting_range[1]:
            intersection_count += 1

# Print the result
print(f"\nIntersection count: {intersection_count}")
