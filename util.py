import random
import os

from numpy.lib.shape_base import column_stack
from pandas.core.frame import DataFrame
from settings import gridsize, debug
from objects import cell

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
        return random.choice(fullcols[:gridsize])
    def rc():
        return random.choice(range(gridsize))
    r = rc()
    c = cl()
    if isinstance(dataframe.at[r, c], cell):
        dataframe.at[r, c] = placee
    else: 
        placeip(dataframe, placee)
    placee.set_loc((r,c))

    return r, c

def placeip_near_wall(dataframe: DataFrame, placee):
    columns_available = fullcols[:gridsize]
    def cl():
        return random.choice([columns_available[0], columns_available[-1]])
    def rc():
        return random.choice(range(gridsize))
    r = rc()
    c = cl()
    if isinstance(dataframe.at[r, c], cell):
        dataframe.at[r, c] = placee
    else: 
        placeip_near_wall(dataframe, placee)
    placee.set_loc((r,c))

    return r, c

def clearconsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

