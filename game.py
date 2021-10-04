import numpy as np
from manager import manager, unitcontroller, placement
from util import placeip, cols, colsandrows, fullcols
from state import state
from objects import player, cell
from visuals import visual
import random

brd = manager()   
st = state()
user = player("P")
control = unitcontroller()
gen = placement(str(random.randint(10000000000, 99999999999)))
vis = visual()


placeip(brd.board, user)
brd.board = gen.generate(brd.board)
control.moverange(user, brd.board)

def get_input():
    action = input("Options:\nmove(up/down/left/right), attack(up/down/left/right).\ninspect(cell), place(cell), his, load(file), exit. \nwhat now?")
    #vis.mainloop()
    def cleaninput(action, ip):
        action = action.replace("{} ".format(ip), "")
        return action

    if "move" in action:
        action = cleaninput(action , "move")
        aclist = action.split(" ")
        step = 1
        if len(aclist) > 1:
            step = int(aclist[1])
        brd.board = control.move(aclist[0], user, brd.board)
        st.save(brd.board)
        control.moverange(user, brd.board)
    
    if "attack" in action:
        action = cleaninput(action , "attack")
        brd.board = control.attack(action, user, brd.board)
        st.save(brd.board)
        print(brd.show())
        #control.moverange(user, brd.board)

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
        user.loc = brd.search("P")
        #for item in brd.board:
        #    item.set_loc(brd.search(item.name))
        print(brd.show())
    vis.window.after(0, get_input)
    
    if "exit" in action:
        vis.window.quit()
        st.close()

vis.window.after(0, get_input)
vis.mainloop()