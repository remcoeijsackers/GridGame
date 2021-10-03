"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.

"""

from random import shuffle
from turtle import Turtle, onscreenclick, tracer, update, ontimer, done
from turtle import setup as setup_turtle


tiles = list(range(64))
state = {'mark': None}
hide = [True] * 64

tt = Turtle()


def square(x, y):
    "Draw white square with black outline at (x, y)."
    tt.up()
    tt.goto(x, y)
    tt.down()
    tt.color('black', 'white')
    tt.begin_fill()
    for count in range(4):
        tt.forward(50)
        tt.left(90)
    tt.end_fill()


def index(x, y):
    "Convert (x, y) coordinates to tiles index."
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    "Convert tiles count to (x, y) coordinates."
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    "Update mark and hidden tiles based on tap."
    spot = index(x, y)
    mark = state['mark']
    print(spot)

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    #else:
    #    hide[spot] = False
    #    hide[mark] = False
    #    state['mark'] = None


def draw():
    "Draw image and tiles."
    tt.clear()
    tt.goto(0, 0)
    tt.stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        tt.up()
        tt.goto(x + 2, y)
        tt.color('black')
        tt.write(tiles[mark], font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 100)


#shuffle(tiles)
setup_turtle(420, 420, 370, 0)
tt.hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()