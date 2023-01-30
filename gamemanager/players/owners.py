from objectmanager.objects.scenery import building
from objectmanager.objects.pawn import pawn
from gamemanager.settings import debug

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

    def startTurn(self):
        """
        Start a player turn.
        """
        if debug:
            print(f"starting turn {self.name}")
        
    def action(self):
        """
        -1 the available action counter for this owner
        """
        self.turns += 1
        self.available_actions -= 1
    
    def clear(self):
        self.available_actions = 2
        self.units = []
        self.buildings = []

