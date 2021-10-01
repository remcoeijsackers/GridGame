import random
import os

from numpy.lib.shape_base import column_stack

cols = ["A","B","C","D","E","F","G","H","I","J"]
rows = [i for i in range(10)]
colsandrows = []
for col in cols:
    cl = []
    for i in range(10):
        cl.append(col)
    colsandrows.append(list(zip(rows, cl)))

def placeip(dataframe, placee):
    def cl():
        return random.choice(cols)
    def rc():
        return random.choice(range(10))
    r = rc()
    c = cl()
    dataframe.at[r, c] = placee
    placee.set_loc((r,c))
    return r, c

def placeclus(dataframe, placee, count):
    colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
    def spread():
        return random.choice([-1,+1])
    def cl():
        return random.choice(cols)
    def rc():
        return random.choice(range(10))
    loc = colsc.get(placee.loc[0]) - 1
    x =  eval('colsr.get(loc[0]) spread()')
    print(x)

def clearconsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

