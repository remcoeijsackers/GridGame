class cell:
    def __init__(self, name = ".") -> None:
        self.name = name
        self.walkable = True
    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

class unit:
    def __init__(self, args) -> None:
        self.name = args[0]
        self.walkrange = 2
        self.steps = []

    def __str__(self) -> str:
        return self.name
    def set_loc(self, loc):
        self.loc = loc
        return self.loc
    

class map_object:
    def __init__(self) -> None:
        pass
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
    def __str__(self) -> str:
        return self.name

class scenery(blockspath):
    def __init__(self, args) -> None:
        super().__init__()
        self.name = args[0]
        self.description = "A Piece of nature, blocking your path"

    def __str__(self) -> str:
        return self.name

class water(scenery):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.name = args[0]
    def __str__(self) -> str:
        return self.name

class player(unit):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.health = 10
