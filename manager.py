import pandas as pd
import random
import os 
from pandas.core.frame import DataFrame


from grid import grid
from util import cols, placeip, clearconsole
from state import state
from objects import cell, unit, map_object, player, scenery, building

class manager:
    def __init__(self) -> None:
        self.board = grid().setup()
        self.__setup()

    def show(self) -> DataFrame:
        return self.board
    
    def __setup(self):
        #placing units
        pla = [unit(i) for i in ["E", "E"]]
        [placeip(self.board, i) for i in pla]

        #placing obstacles
        plb = [building(i) for i in ["B" for i in range(random.randint(1,6))]]
        [placeip(self.board, i) for i in plb] 

        #placing scenery
        pls = [scenery(i) for i in ["T" for i in range(random.randint(1,6))]]
        [placeip(self.board, i) for i in pls]  

    def inspect(self, loc):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        pr = colsc.get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        print(contents.description)
        return contents
    
    def search(self, loc, item):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        pr = colsc.get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        #print(str(contents))
        if item == str(contents):
            return loc
        else: 
            pass


class unitcontroller:
    def __init__(self) -> None:
        pass

    def count(self, unit, loc) -> int:
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        z = unit.loc[0], colsc.get(unit.loc[1])
        b = int(loc[0]), colsc.get(loc[1])
        outcome = abs(z[0] - b[0]) + abs(z[1] - b[1])
        return outcome
       

    def place(self, unit, loc, board: DataFrame) -> DataFrame:
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        pr = colsc.get(loc[1])
        ul = colsc.get(unit.loc[1])
        distance = self.count(unit, loc)
        if distance <= unit.range:
            print("{} is walking {} steps".format(unit.name, distance))
            newboard = board
            newboard.iloc[int(unit.loc[0])][int(ul)] = cell() 
            newboard.iloc[int(loc[0])][int(pr)] = unit 
            unit.set_loc((int(loc[0]),loc[1]))
            return newboard
        else:
            print("{} has max range of {}".format(unit.name, unit.range))
            return board

    def move(self, direction, unit, board) -> DataFrame:
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        colsr = dict(zip(list(range(10)), cols)) # for mapping ints to colname
        y, x = unit.loc[0],unit.loc[1]
        def __moveandclean(y,x):
            board.at[unit.loc[0], unit.loc[1]] = cell() #clean old position
            board.at[y, x] = unit
            unit.set_loc((y,x))
        if direction == "up" and y != 0:
                y -= int(unit.steps)
                if getattr(board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "down" and y != 9:
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

    def moverange(self, unit, board):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        colsr = dict(zip(list(range(10)), cols)) # for mapping ints to colname
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
        if (y != 0 and y != 9) or (x != "A" and x != "J"):
            if y != 0 and y != 9:
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
            if y != 0 and y != 9:
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

    