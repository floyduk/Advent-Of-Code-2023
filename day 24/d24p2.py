from z3 import IntVector, Solver

# open and read the input file into a list of strings
input = open("input.txt", "r").read().split("\n")

# Number of hailstones to solve for
num_to_solve_for = 3

# Import the data into a simple list of tuples (x, y, z, dx, dy, dz)
hailstones = []
for line in input:
    position, direction = line.split(" @ ")
    hailstones.append(tuple([int(a) for a in position.split(", ")] + [int(a) for a in direction.split(", ")]))

# Set up the solution values we want out of Z3
sx, sy, sz, sdx, sdy, sdz = IntVector("solution", 6)
hail = IntVector("hailstones", num_to_solve_for)
solver = Solver()

# Load in the first num_to_solve_for hailstones.
for target, (x, y, z, dx, dy, dz) in zip(hail, hailstones[:num_to_solve_for]):
    solver.add(sx + target * sdx == x + target * dx)
    solver.add(sy + target * sdy == y + target * dy)
    solver.add(sz + target * sdz == z + target * dz)

# Press go on the solver
solver.check()
model = solver.model()

# Print the result
print(f"{model[sx]}, {model[sy]}, {model[sz]}")
print(f"Solving for {num_to_solve_for} hailstones: {sum(model[a].as_long() for a in (sx, sy, sz))}")