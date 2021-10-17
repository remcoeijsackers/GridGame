import pandas as pd
import random
import os 
from pandas.core.frame import DataFrame


from grid import grid
from util import cols, fullcols, placeip, clearconsole, colsandrows, colsc, colsr, rows
from state import state
from objects import cell, unit, map_object, player, scenery, building, broken_cell
from settings import gridsize, debug

class placement:
    def __init__(self, seed: str) -> None:
        self.seed = seed
        self.coreseed = seed[:len(seed)//2]
        self.subseed = seed[len(seed)//2:]

    def placeip(self, board, placee):
        for i,x in list(zip(self.coreseed, self.subseed)):
            def cl():
                random.seed(int(i))
                return random.choice(fullcols[:gridsize])
            def rc():
                random.seed(int(x))
                return random.choice(range(gridsize))
            r = rc()
            c = cl()
            if hasattr(board.at[r, c], 'walkable'):
                board.at[r, c] = placee
            else: 
                placeip(board, placee)
            placee.set_loc((r,c))
            if debug:
                print(r,c)
        return r, c

    def generate(self, board):
        #placing units
        #pla = [unit(i) for i in ["E", "E"]]
        #[placeip(self.board, i) for i in pla]

        #placing obstacles
        #random.seed(int(self.coreseed))
        plb = [building(i) for i in ["B" for i in range(random.randint(1,6))]]
        #[self.placeip(board, i) for i in plb] 

        #placing scenery
        #random.seed(int(self.subseed))
        pls = [scenery(i) for i in ["T" for i in range(random.randint(1,6))]]
        [self.placeip(board, i) for i in pls]  
        return board

class manager:
    def __init__(self) -> None:
        self.board = grid().setup()
        #self.__setup()

    def show(self) -> DataFrame:
        return self.board
    
    def modify(self, board) -> None:
        self.board = board 

    def __setup(self):
        #placing units
        #pla = [unit(i) for i in ["E", "E"]]
        #[placeip(self.board, i) for i in pla]

        #placing obstacles
        plb = [building(i) for i in ["B" for i in range(random.randint(1,6))]]
        [placeip(self.board, i) for i in plb] 

        #placing scenery
        pls = [scenery(i) for i in ["T" for i in range(random.randint(1,6))]]
        [placeip(self.board, i) for i in pls]  

    def inspect(self, loc):
        pr = colsc.get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        return contents

    def explain(self, loc):
        pr = colsc.get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        return contents.description
    
    def search(self, item):
        # loop trough the entire dataframe until there is a match on name, then return the location
        for loclist in colsandrows:
            for loc in loclist:
                pr = colsc.get(loc[1])
                contents = self.board.iloc[int(loc[0])][int(pr)]
                if item == str(contents):
                    return loc
                    
    def getstats(self, loc):
        pr = colsc.get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        if hasattr(contents, 'health'):
            return str(contents.health)
        else: 
            return ""
    
    def broken_tiles(self, board: DataFrame):
        for spot in colsandrows:
            for coord in spot:
                if isinstance(board.at[coord[0], coord[1]], broken_cell):
                    yield coord
    
    def is_adjacent(self, board: DataFrame, item1, item2):
        # check if something is adjacent to something else, in a square grid (including vertical)
        pass



class unitcontroller:
    def __init__(self) -> None:
        pass

    def count(self, unit, loc) -> int:
        z = unit.loc[0], colsc.get(unit.loc[1])
        b = int(loc[0]), colsc.get(loc[1])
        # for singular vertical moves
        if abs(z[0] - b[0]) ==  1 and abs(z[1] - b[1]) == 1:
            # both are one
            outcome = 1
        elif (abs(z[0] - b[0]) !=  1 and abs(z[1] - b[1]) != 1) and abs(z[0] - b[0]) == abs(z[1] - b[1]):
            #both are the same, but not one
            outcome = abs(z[0] - b[0])

        else: 
            outcome = abs(z[0] - b[0]) + abs(z[1] - b[1])
        return outcome
    
    def possible_moves(self, unit, board: DataFrame):
        for spot in colsandrows:
            for coord in spot:
                if self.count(unit, coord) <= unit.range and getattr(board.at[coord[0], coord[1]], 'walkable'):
                    yield coord
    
    def possible_melee_moves(self, unit, board: DataFrame):
        for spot in colsandrows:
            for coord in spot:
                if self.count(unit, coord) <= unit.melee_range and getattr(board.at[coord[0], coord[1]], 'walkable'):
                    yield coord

    def place(self, unit, loc, board: DataFrame) -> DataFrame:
        pr = colsc.get(loc[1])
        ul = colsc.get(unit.loc[1])
        distance = self.count(unit, loc)
        if distance <= unit.range:
            if getattr(board.at[loc[0], loc[1]], 'walkable'):
                print("{} is walking {} steps".format(unit.name, distance))
                newboard = board
                newboard.iloc[int(unit.loc[0])][int(ul)] = cell() 
                newboard.iloc[int(loc[0])][int(pr)] = unit 
                unit.set_loc((int(loc[0]),loc[1]))
                return newboard
            else:
                print("{} can't move there".format(unit.name))
                return board
        else:
            print("{} has max range of {}".format(unit.name, unit.range))
            return board

    def move(self, direction, unit, board: DataFrame) -> DataFrame:
        y, x = unit.loc[0],unit.loc[1]
        def __moveandclean(y,x):
            board.at[unit.loc[0], unit.loc[1]] = cell() #clean old position
            board.at[y, x] = unit
            unit.set_loc((y,x))
            
        if direction == "up" and y != 0:
                y -= int(unit.steps)
                if getattr(board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "down" and y != max(rows):
                y += int(unit.steps)
                if getattr(board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "left" and x != "A":
                loc = colsc.get(x) - unit.steps
                x = colsr.get(loc)
                if getattr(board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "right" and x != "J":
                loc = colsc.get(x) + unit.steps
                x = colsr.get(loc)
                if getattr(board.at[y, x], 'walkable'):
                    __moveandclean(y,x)
        return board
    
    def attack(self, loc, board) -> DataFrame:
        pr = colsc.get(loc[1])
        def __break():
            board.iloc[int(loc[0])][int(pr)] = broken_cell()

        if getattr(board.iloc[int(loc[0])][int(pr)], 'walkable'):
            __break()

        return board
    
    def attack_on_loc(self, loc, board):
        pr = colsc.get(loc[1])
        def __break():
            board.iloc[int(loc[0])][int(pr)] = broken_cell()

        if getattr(board.iloc[int(loc[0])][int(pr)], 'walkable'):
            __break()

        return board

    def moverange(self, unit, board):
        y, x = unit.loc[0],unit.loc[1]
        z = y - unit.steps
        p = y + unit.steps
        loc = colsc.get(x) - unit.steps
        locx = colsr.get(loc)
        loc1 = colsc.get(x) + unit.steps
        locx1 = colsr.get(loc1)
        zp = [z,p]
        ll = [locx, locx1]
        subboard = board
        if (y != 0 and y != max(rows)) or (x != "A" and x != "J"):
            if y != 0 and y != max(rows):
                # Show to cells the unit can walk
                for i in zp:
                    # top and bottom
                    if isinstance(subboard.at[i, x], cell):
                        subboard.at[i, x] = cell(name="%")
            if x != "A" and x != "J":
                for i in ll:
                    # left and right
                    if isinstance(subboard.at[y, i], cell):
                        subboard.at[y, i] = cell(name="%")
            print(subboard)
            # clean up the cells
            if y != 0 and y != max(rows):
                for i in zp:
                    if isinstance(subboard.at[i, x], cell):
                        subboard.at[i, x] = cell(name=".")
            if x != "A" and x != "J":
                for i in ll:
                    if isinstance(subboard.at[y, i], cell):
                        subboard.at[y, i] = cell(name=".")
        else:
            print(board)

class unitbrain:
    def __init__(self) -> None:
        pass

    