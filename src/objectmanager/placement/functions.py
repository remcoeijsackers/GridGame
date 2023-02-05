import random
from pandas.core.frame import DataFrame

from src.objectmanager.objects.grid import cell
from src.gamemanager.settings import gridsize
from src.contexts.settingscontext import placement_details_context

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
        for _ in range(gridsize.get_gridsize()):
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

def getColFromDirection(place):
        if place == "left":
            return fullcols[0]
        if place == "right":
            return fullcols.copy().pop()
        if place == "center":
            return fullcols[:int(gridsize.get_gridsize()/2)].pop()
        if place == "fuzzy":
            return random.choice(fullcols[:gridsize.get_gridsize()])  
        return None

def getRowFromDirection(place):
        if place == "top":
            return 0
        if place == "bottom":
            return gridsize.get_gridsize() -1
        if place == "center":
            return abs(gridsize.get_gridsize()/2)
        if place == "fuzzy": 
            return random.choice(range(gridsize.get_gridsize()))
        return None

def getRowAndColFromDirectionContext(placemetDetails:placement_details_context):
    if placemetDetails.specific:
        if placemetDetails.compass == "left" or "right":
            col = getColFromDirection(placemetDetails.compass)
        if placemetDetails.compass == "top" or "bottom":
            row = getRowFromDirection(placemetDetails.compass)
        if col == None:
            col = getColFromDirection(placemetDetails.details)
        if row == None:
            row = getRowFromDirection(placemetDetails.details)
    if placemetDetails.mode == "fuzzy":
        col = getColFromDirection("fuzzy")
        row = getRowFromDirection("fuzzy")
    
    return row, col
    
def placementHandler(dataframe, placee, placemetDetails: placement_details_context):

    def handlePlacement(r, c):
        if isinstance(dataframe.at[r, c], cell) and bool(getattr(dataframe.at[r,c], 'walkable')):
            dataframe.at[r, c] = placee
            placee.set_loc((r,c))
            return True
        else: 
            placeip(dataframe, placee)
            return False

    r, c = getRowAndColFromDirectionContext(placemetDetails)
    return handlePlacement(r, c)


def placeipRigid(dataframe, placee, place):
    def cl():
        if place == "left":
            return fullcols[0]
        if place == "right":
            return fullcols.copy().pop()
        if place == "center":
            return fullcols[:abs(gridsize.get_gridsize()/2)]
        else:
            return random.choice(fullcols[:gridsize.get_gridsize()])
    def rc():
        if place == "top":
            return 0
        if place == "bottom":
            return gridsize.get_gridsize() -1
        if place == "center":
            return abs(gridsize.get_gridsize()/2)
        else: 
            return random.choice(range(gridsize.get_gridsize()))
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

def placeclus(brd, placee):
    """
    Place a cluster around an object.
    Creates new instances of the objects class.
    """
    classfromobject = placee.__class__
    name = placee.name
    placeip_near_wall(brd.board, placee)
    for i in brd.get_adjacent_cells(placee.loc, 2):
        x = classfromobject(name)
        if  isinstance(brd.board.at[i[0], i[1]], cell) and bool(getattr(brd.board.at[i[0],i[1]], 'walkable')): #hasattr(self.board.at[i[0],i[1]], 'walkable') and 
            brd.board.at[i[0], i[1]] = x
            x.set_loc((i[0], i[1]))