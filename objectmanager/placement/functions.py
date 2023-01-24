import random
import os

from pandas.core.frame import DataFrame
from objectmanager.objects.grid import cell
from gamemanager.settings import gridsize

symbol_thickness = 40
unit_thickness = 10

cols = ["A","B","C","D","E","F","G","H","I","J"]
fullcols = [i for i in "abcdefghijklmnopqrstuvwxyz".upper()]

def colsc():
    """
    For mapping letters to ints.
    """
    return dict(zip(fullcols[:gridsize.get_gridsize()], list(range(gridsize.get_gridsize())))) #for mapping colname to ints
def colsr():
    """
    For mapping ints to letters.
    """
    return dict(zip(list(range(gridsize.get_gridsize())), fullcols[:gridsize.get_gridsize()])) # for mapping ints to colname

def rows():
    return [i for i in range(gridsize.get_gridsize())]

def colsandrows():
    colsandrows_ls = []
    for col in fullcols[:gridsize.get_gridsize()]:
        cl = []
        for i in range(gridsize.get_gridsize()):
            cl.append(col)
        colsandrows_ls.append(list(zip(rows(), cl)))
    return colsandrows_ls

def placeip(dataframe, placee):
    def cl():
        return random.choice(fullcols[:gridsize.get_gridsize()])
    def rc():
        return random.choice(range(gridsize.get_gridsize()))
    r = rc()
    c = cl()
    if  isinstance(dataframe.at[r, c], cell) and bool(getattr(dataframe.at[r,c], 'walkable')):
        dataframe.at[r, c] = placee
        placee.set_loc((r,c))
    else: 
        placeip(dataframe, placee)

    return r, c

def placeipRigid(dataframe, placee, place):
    columns_available = fullcols[:gridsize.get_gridsize()]
    def cl():
        return random.choice(fullcols[:gridsize.get_gridsize()])
    def rc():
        if place == "top":
            return 0
        if place == "bottom":
            return gridsize.get_gridsize() -1
    r = rc()
    c = cl()
    if isinstance(dataframe.at[r, c], cell) and bool(getattr(dataframe.at[r,c], 'walkable')):
        dataframe.at[r, c] = placee
        placee.set_loc((r,c))
    else: 
        placeipRigid(dataframe, placee, place)

def placeip_near_wall(dataframe: DataFrame, placee):
    columns_available = fullcols[:gridsize.get_gridsize()]
    def cl():
        return random.choice([columns_available[0], columns_available[-1]])
    def rc():
        return random.choice(range(gridsize.get_gridsize()))
    r = rc()
    c = cl()
    if isinstance(dataframe.at[r, c], cell):
        dataframe.at[r, c] = placee
        placee.set_loc((r,c))
    else: 
        placeip_near_wall(dataframe, placee)
    
    return r, c