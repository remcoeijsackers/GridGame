import random
from objectmanager.objects.piece import boardItem
watercolors = ['#0e1b7d', '#1b2785', '#141f7a']

class blockspath(boardItem):
    def __init__(self) -> None:
        self.walkable = False
        super().__init__()
        
class building(blockspath):
    def __init__(self, args) -> None:
        super().__init__()
        self.name = args[0]
        self.description = "A house"
        self.color = '#E0f9FF'

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

    def __str__(self) -> str:
        return self.name

class water(scenery):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.name = args[0]
        self.color = random.choice(watercolors)

    def __str__(self) -> str:
        return self.name

