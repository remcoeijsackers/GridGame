from src.objects import building
from objectmanager.objects.pawn import pawn

class owner:
    """
    Reflects the user controlling the units.
    """
    def __init__(self, id, name, color: str) -> None:
        self.id = id
        self.name = name
        self.color = color

        self.available_actions = 2
        self.units:list(pawn) = []
        
        self.buildings: list(building) = []
        self.control = "manual"
        self.turns = 0
    
    def __repr__(self) -> str:
        return self.name

    def setContol(self, controlType):
        self.control = controlType
        
    def action(self):
        self.turns += 1
        self.available_actions -= 1
    
    def clear(self):
        self.available_actions = 2
        self.units = []
        self.buildings = []

