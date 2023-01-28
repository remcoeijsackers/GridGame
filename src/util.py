import random
import os

from pandas.core.frame import DataFrame
from objectmanager.objects.grid import cell
from gamemanager.settings.settings import gridsize

symbol_thickness = 40
unit_thickness = 10

cols = ["A","B","C","D","E","F","G","H","I","J"]
fullcols = [i for i in "abcdefghijklmnopqrstuvwxyz".upper()]

def getDiagonalLine(loc, direction=["all"]):
    locsBotL = [loc]
    locsBotR = [loc]
    locsTopL = [loc]
    locsTopR = [loc]
    locsLeft = [loc]
    locsRight = [loc]
    locsTop = [loc]
    locsBottom = [loc]

    def __bottom(i):
        return bottom(locsBottom[i])
    def __top(i):
        return top(locsTop[i])
    def __right(i):
        return right(locsRight[i])
    def __left(i):
        return left(locsLeft[i])

    def __botL(i):
        return bottomL(locsBotL[i])

    def __topR(i):
        return topR(locsTopR[i])

    def __botR(i):
        return bottomR(locsBotR[i])

    def __topL(i):
        return topL(locsTopL[i])

    for i in range(30):
        if __right(i):
            locsRight.append(__right(i))
        else:
            break

    for i in range(30):
        if __left(i):
            locsLeft.append(__left(i))
        else:
            break

    for i in range(30):
        if __bottom(i):
            locsBottom.append(__bottom(i))
        else:
            break

    for i in range(30):
        if __top(i):
            locsTop.append(__top(i))
        else:
            break
    
    for i in range(30):
        if __topR(i):
            locsTopR.append(__topR(i))
        else:
            break

    for i in range(30):
        if __botL(i):
            locsBotL.append(__botL(i))
        else: 
            break

    for i in range(30):
        if __botR(i):
            locsBotR.append(__botR(i))
        else: 
            break

    for i in range(30):
        if __topL(i):
            locsTopL.append(__topL(i))
        else: 
            break
    
    finalLocs = []
    for i in locsBotL:
        if i != loc and "all" in direction or "bottomleft" in direction:
            finalLocs.append(i)
    for i in locsBotR:
        if i != loc and "all" in direction or "bottomright" in direction:
            finalLocs.append(i)
    for i in locsTopL:
        if i != loc and "all" in direction or "topleft" in direction:
            finalLocs.append(i)
    for i in locsTopR:
        if i != loc and "all" in direction or "topright" in direction:
            finalLocs.append(i)
    for i in locsTop:
        if i != loc and "all" in direction or "top" in direction:
            finalLocs.append(i)
    for i in locsBottom:
        if i != loc and "all" in direction or "bottom" in direction:
            finalLocs.append(i)
    for i in locsRight:
        if i != loc and "all" in direction or "right" in direction:
            finalLocs.append(i)
    for i in locsLeft:
        if i != loc and "all" in direction or "left" in direction:
            finalLocs.append(i)


    return finalLocs

def top(loc):
    if loc[0] - 1 >= 0:
        r1 = loc[0] - 1
    else:
        return None
    r2 = loc[1]
    return (r1, r2)

def bottom(loc):
    if loc[0] + 1 <= gridsize.get_gridsize():
        r1 = loc[0] + 1
    else:
        return None
    r2 = loc[1]
    return (r1, r2)

def left(loc):
    r1 = loc[0]
    if colsr().get(colsc().get(loc[1]) - 1):
        r2 = colsr().get(colsc().get(loc[1]) - 1)
    else: 
        return None
    return (r1, r2)

def right(loc):
    r1 = loc[0]
    if colsr().get(colsc().get(loc[1]) + 1):
        r2 = colsr().get(colsc().get(loc[1]) + 1)
    else:
        return None
    return (r1, r2)

def topR(loc):
    if loc[0] - 1 >= 0:
        r1 = loc[0] - 1
    else:
        return None
    if colsr().get(colsc().get(loc[1]) + 1):
        r2 = colsr().get(colsc().get(loc[1]) + 1)
    else:
        return None
    return (r1, r2)

def topL(loc):
    if loc[0] - 1 >= 0:
        r1 = loc[0] - 1
    else:
        return None
    if colsr().get(colsc().get(loc[1]) - 1):
        r2 = colsr().get(colsc().get(loc[1]) - 1)
    else:
        return None
    return (r1, r2)

def bottomR(loc):
    if loc[0] + 1 <= gridsize.get_gridsize():
        r1 = loc[0] + 1
    else:
        return None
    if colsr().get(colsc().get(loc[1]) + 1):
        r2 = colsr().get(colsc().get(loc[1]) + 1)
    else: 
        return None
    return (r1, r2)

def bottomL(loc):
    if loc[0] + 1 <= gridsize.get_gridsize():
        r1 = loc[0] + 1
    else:
        return None
    if colsr().get(colsc().get(loc[1]) - 1):
        r2 = colsr().get(colsc().get(loc[1]) - 1)
    else:
        return None
    return (r1, r2)

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

def clearconsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

