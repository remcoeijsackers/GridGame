class cell:
    def __init__(self, name = ".") -> None:
        self.name = name
        self.walkable = True
        self.description = "a cell on the grid"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

class broken_cell:
    def __init__(self, name = "x") -> None:
        self.name = name
        self.walkable = False
        self.description = "a broken cell on the grid"
        self.destroyed = False

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

class unit:
    def __init__(self, args) -> None:
        self.name = args[0]
        self.description = "{}".format(self.name)
        self.range = 1
        self.steps = 1
        self.melee_range = 1
        self.walkable = False
        self.health = 3
        self.destroyed = False
        self.strength = 1

    def __str__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroyed = True

    

class map_object:
    def __init__(self) -> None:
        self.name = ""
    def __repr__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc

class blockspath(map_object):
    def __init__(self) -> None:
        self.walkable = False
        
class building(blockspath):
    def __init__(self, args) -> None:
        super().__init__()
        self.name = args[0]
        self.description = "A house"
        self.destroyed = False
    def __str__(self) -> str:
        return self.name
    def set_loc(self, loc):
        self.loc = loc
        return self.loc

class scenery(blockspath):
    def __init__(self, args) -> None:
        super().__init__()
        self.name = args[0]
        self.description = "A Piece of nature, blocking your path"
        self.destroyed = False

    def __str__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc

class water(scenery):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.name = args[0]
    def __str__(self) -> str:
        return self.name

class player(unit):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.description = "The player"

class enemy(unit):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.health = 10
        self.description = "An Enemy"
