import pyximport

pyximport.install()

import aocd
import q24c

data = aocd.get_data(day=24, year=2021).split("inp w")[1:]
a_vars = [int(prog.splitlines()[1:][4].split()[-1]) for prog in [prog for prog in data]]
b_vars = [int(prog.splitlines()[1:][14].split()[-1]) for prog in [prog for prog in data]]
q24c.init_globals(a_vars, b_vars)
p1 = q24c.solve(0, 0, 1)
print("Part 1: ", p1)
q24c.init_globals(a_vars, b_vars)
p2 = q24c.solve(0, 0, 0)
print("Part 2: ", p2)
