class cell:
    def __init__(self, name = ".", stepped_on=0) -> None:
        self.name = name
        self.walkable = True
        self.description = "a cell on the grid"
        self.stepped_on = stepped_on

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc

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
        self.fullname = None

    def __str__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc

    def set_image(self, image):
        self.image = image
        return self.image
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroyed = True

class player(unit):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.description = "A unit"

class enemy(unit):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.health = 4
        self.description = "An NPC, hostile"
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
        self.color = '#E0f9FF'
        self.owner = None
    def __str__(self) -> str:
        return self.name
    def set_loc(self, loc):
        self.loc = loc
        return self.loc

    def set_owner(self, owner):
        self.owner = owner
        return self.owner

    def set_color(self, color):
        self.color = color
        return self.color

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
    
    def get_class_r(self, args):
        return scenery(args[0])

class tree(scenery):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.name = args[0]
        self.destroyed = False
    def __str__(self) -> str:
        return self.name
class water(scenery):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.name = args[0]
        self.destroyed = False
    def __str__(self) -> str:
        return self.name

