import random
import os

from numpy.lib.shape_base import column_stack
from settings import gridsize, debug

cols = ["A","B","C","D","E","F","G","H","I","J"]
fullcols = [i for i in "abcdefghijklmnopqrstuvwxyz".upper()]

colsc = dict(zip(fullcols[:gridsize], list(range(gridsize)))) #for mapping colname to ints

colsr = dict(zip(list(range(gridsize)), fullcols[:gridsize])) # for mapping ints to colname

rows = [i for i in range(gridsize)]

colsandrows = []
for col in fullcols[:gridsize]:
    cl = []
    for i in range(gridsize):
        cl.append(col)
    colsandrows.append(list(zip(rows, cl)))

def placeip(dataframe, placee):
    def cl():
        return random.choice(cols)
    def rc():
        return random.choice(range(gridsize))
    r = rc()
    c = cl()
    if hasattr(dataframe.at[r, c], 'walkable'):
        dataframe.at[r, c] = placee
    else: 
        placeip(dataframe, placee)
    placee.set_loc((r,c))
    if debug:
        print(r,c)
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

