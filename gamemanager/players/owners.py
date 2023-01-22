from src.objects import building
from objectmanager.objects.pawn import pawn

class owner:
    """
    Reflects the user controlling the units.
    """
    def __init__(self, name, color) -> None:
        self.name = name
        self.available_actions = 2
        self.units:list(pawn) = []
        self.color = color
        self.buildings: list(building) = []
        self.control = "manual"
        self.openTurn = True
    
    def startTurn(self):
        self.openTurn = True
        if self.control == "manual":
            return ["manual", self.name]

        if self.control == "computer":
            return ["auto", self.name]

    def endTurn(self):
        self.openTurn = False

    def setContol(self, controlType):
        self.control = controlType
        
    def action(self):
        self.available_actions -= 1
    
    def clear(self):
        self.available_actions = 2
        self.units = []
        self.buildings = []

