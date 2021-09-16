import pandas as pd
import random
import os 

from pandas.core.frame import DataFrame
from util import cols 
from util import placeip
from objects import cell, unit, map_object, player, scenery, building

class grid:
    def __init__(self) -> None:
        self.base_grid = []

    def setup(self) -> DataFrame:
        grd = []
        [grd.append(cell()) for i in range(10)]
        [self.base_grid.append(grd) for i in range(10)]
        
        df = pd.DataFrame(self.base_grid, columns=cols)
        return df

class game:
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
        if y != 0 and y != 9 and x != "A" and x != "J":
            for i in zp:
                if isinstance(self.board.at[i, x], cell):
                    self.board.at[i, x] = cell(name="%")

            for i in ll:
                if isinstance(self.board.at[y, i], cell):
                    self.board.at[y, i] = cell(name="%")
            print(self.board)
            for i in zp:
                self.board.at[i, x] = cell(name=".")
            for i in ll:
                self.board.at[y, i] = cell(name=".")

        
    def move(self, direction, unit, steps = 1):
        colsc = dict(zip(cols, list(range(10)))) #for mapping colname to ints
        colsr = dict(zip(list(range(10)), cols)) # for mapping ints to colname
        y, x = unit.loc[0],unit.loc[1]
        self.moverange(user)
        def __moveandclean(y,x):
            self.board.at[unit.loc[0], unit.loc[1]] = cell() #clean old position
            self.board.at[y, x] = unit
            unit.set_loc((y,x))
        if direction == "up" and y != 0:
                y -= steps
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)
        if direction == "down" and y != 9:
                y += steps
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)
        if direction == "left" and x != "A":
                loc = colsc.get(x) - steps
                x = colsr.get(loc)
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)
        if direction == "right" and x != "J":
                loc = colsc.get(x) + steps
                x = colsr.get(loc)
                if getattr(self.board.at[y, x], 'walkable'):
                    __moveandclean(y,x)

        return self.board

class state:
    def __init__(self) -> None:
        self.his = []
        self.v = 0

    def save(self, board):
        self.v += 1
        board.to_pickle("saves/"+str(self.v))
        di = (self.v, board)
        self.his.append(di)

    def load(self, v) -> DataFrame:
        df2 = pd.read_pickle("saves/{}".format(v))
        return df2

brd = game()   
st = state()
user = player("P")
placeip(brd.board, user)
print(brd.moverange(user))

while True:
    action = input("Options: move(up/down/left/right) inspect(cell) \nwhat now?")
    def cleaninput(action, ip):
        action = action.replace("{} ".format(ip), "")
        return action
    if "move" in action:
        action = cleaninput(action , "move")
        aclist = action.split(" ")
        step = 1
        if len(aclist) > 1:
            step = int(aclist[1])
        st.save(brd.move(aclist[0],user, step))
        print(brd.moverange(user))
    if "inspect" in action:
        action = cleaninput(action, "inspect")
        brd.inspect(action)
    if "his" in action:
        print(st.his)
        print("\n")
    if "load" in action:
        action = cleaninput(action, "load")
        brd.board = st.load(action)
        print(brd.show())
    if "exit" in action:
        for i in range(st.v):
            os.remove('saves/{}'.format(i+1))
            exit(0)
    

    
