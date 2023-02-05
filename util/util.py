from gamemanager.settings.settings import gridsize

symbol_thickness = 40
unit_thickness = 10

cols = ["A","B","C","D","E","F","G","H","I","J"]
fullcols = [i for i in "abcdefghijklmnopqrstuvwxyz".upper()]

def getCoordLine(loc, direction=["all"]) -> list:
    """
    Get a list of coordinates, in a straight line.
    Given a starting location and a direction.
    """
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
        if __left(i) and __left(i)[0] <= gridsize.get_gridsize() -1:
            locsLeft.append(__left(i))
        else:
            break

    for i in range(30):
        if __bottom(i) and __bottom(i)[0] <= gridsize.get_gridsize() -1:
            locsBottom.append(__bottom(i))
        else:
            break

    for i in range(30):
        if __top(i) and __top(i)[0] <= gridsize.get_gridsize() -1:
            locsTop.append(__top(i))
        else:
            break
    
    for i in range(30):
        if __topR(i) and __topR(i)[0] <= gridsize.get_gridsize() -1:
            locsTopR.append(__topR(i))
        else:
            break

    for i in range(30):
        if __botL(i) and __botL(i)[0] <= gridsize.get_gridsize() -1:
            locsBotL.append(__botL(i))
        else: 
            break

    for i in range(30):
        if __botR(i) and __botR(i)[0] <= gridsize.get_gridsize() -1:
            locsBotR.append(__botR(i))
        else: 
            break

    for i in range(30):
        if __topL(i) and __topL(i)[0] <= gridsize.get_gridsize() -1:
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
    """
    get the loc above the given loc.
    """
    if loc[0] - 1 >= 0:
        r1 = loc[0] - 1
    else:
        return None
    r2 = loc[1]
    return (r1, r2)

def bottom(loc):
    """
    get the loc below the given loc.
    """
    if loc[0] + 1 <= gridsize.get_gridsize():
        r1 = loc[0] + 1
    else:
        return None
    r2 = loc[1]
    return (r1, r2)

def left(loc):
    """
    get the loc left from the given loc.
    """
    r1 = loc[0]
    if colsr().get(colsc().get(loc[1]) - 1):
        r2 = colsr().get(colsc().get(loc[1]) - 1)
    else: 
        return None
    return (r1, r2)

def right(loc):
    """
    get the loc right from the given loc.
    """
    r1 = loc[0]
    if colsr().get(colsc().get(loc[1]) + 1):
        r2 = colsr().get(colsc().get(loc[1]) + 1)
    else:
        return None
    return (r1, r2)

def topR(loc):
    """
    get the loc top right from the given loc.
    """
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
    """
    get the loc top left from the given loc.
    """
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
    """
    get the loc bottom right from the given loc.
    """
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
    """
    get the loc bottom left from the given loc.
    """
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
    """
    return all rows.
    """
    return [i for i in range(gridsize.get_gridsize())]

def colsandrows():
    """
    return all cols and rows.
    """
    colsandrows_ls = []
    for col in fullcols[:gridsize.get_gridsize()]:
        cl = []
        for _ in range(gridsize.get_gridsize()):
            cl.append(col)
        colsandrows_ls.append(list(zip(rows(), cl)))
    return colsandrows_ls


