from gamemanager.dm import gameController
from gamemanager.players.owners import owner
from src.context import color_context

if __name__ == "__main__":
    pl1 = owner(1, "henk", color_context().red_color)
    pl2 = owner(2, "jaap", color_context().red_color)
    pl3 = owner(3, "piet", color_context().red_color)

    game = gameController([pl1,pl2,pl3])

    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")
    game.playerAction("")

