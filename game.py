import numpy as np
from manager import manager, unitcontroller
from util import placeip
from state import state
from objects import player, cell

brd = manager()   
st = state()
user = player("P")
control = unitcontroller()
placeip(brd.board, user)
control.moverange(user, brd.board)

while True:
    action = input("Options: move(up/down/left/right) inspect(cell) place(cell) his load(file) \nwhat now?")

    def cleaninput(action, ip):
        action = action.replace("{} ".format(ip), "")
        return action

    if "move" in action:
        action = cleaninput(action , "move")
        aclist = action.split(" ")
        step = 1
        if len(aclist) > 1:
            step = int(aclist[1])
        #st.save(brd.move(aclist[0],user))
        #brd.move(aclist[0],user)
        brd.board = control.move(aclist[0], user, brd.board)
        st.save(brd.board)
        control.moverange(user, brd.board)

    if "place" in action:
        action = cleaninput(action, "place")
        brd.board = control.place(user, action, brd.board)
        print(brd.show())

    if "inspect" in action:
        action = cleaninput(action, "inspect")
        brd.inspect(action)

    if "his" in action:
        print(st.his)
        print("\n")

    if "load" in action:
        action = cleaninput(action, "load")
        brd.board = st.load(action)
        #print(user.loc)
        #nn = brd.board.to_numpy()
        print(brd.show())

    if "exit" in action:
        st.close()
