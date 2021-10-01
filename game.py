from manager import manager
from util import placeip
from state import state
from objects import player

brd = manager()   
st = state()
user = player("P")
placeip(brd.board, user)
print(brd.show())

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
        #st.save(brd.move(aclist[0],user))
        brd.move(aclist[0],user)
        #print(brd.show())
        brd.moverange(user)
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
        st.close()