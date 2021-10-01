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

    def moverange(self, unit):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        colsr = dict(zip(list(range(10)), cols)) # for mapping ints to colname
        y, x = unit.loc[0],unit.loc[1]
        z = y - 1 
        p = y + 1
        loc = colsc.get(x) - 1
        locx = colsr.get(loc)
        loc1 = colsc.get(x) + 1
        locx1 = colsr.get(loc1)
        zp = [z,p]
        ll = [locx, locx1]
        subboard = self.board
        if y != 0 and y != 9 and x != "A" and x != "J":
            # Show to cells the unit can walk
            for i in zp:
                # top and bottom
                if isinstance(subboard.at[i, x], cell):
                    subboard.at[i, x] = cell(name="%")

            for i in ll:
                # left and right
                if isinstance(subboard.at[y, i], cell):
                    subboard.at[y, i] = cell(name="%")
            print(subboard)
            # clean up the cells
            for i in zp:
                if isinstance(subboard.at[i, x], cell):
                    subboard.at[i, x] = cell(name=".")
            for i in ll:
                if isinstance(subboard.at[y, i], cell):
                    subboard.at[y, i] = cell(name=".")

        
    def move(self, direction, unit):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        colsr = dict(zip(list(range(10)), cols)) # for mapping ints to colname
        y, x = unit.loc[0],unit.loc[1]
        def __moveandclean(y,x):
            self.board.at[unit.loc[0], unit.loc[1]] = cell() #clean old position
            self.board.at[y, x] = unit
            unit.set_loc((y,x))
        if direction == "up" and y != 0:
                y -= unit.steps
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "down" and y != 9:
                y += unit.steps
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "left" and x != "A":
                loc = colsc.get(x) - unit.steps
                x = colsr.get(loc)
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        if direction == "right" and x != "J":
                loc = colsc.get(x) + unit.steps
                x = colsr.get(loc)
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        return self.board
    





    