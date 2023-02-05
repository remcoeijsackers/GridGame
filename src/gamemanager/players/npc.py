from src.gamemanager.players.owners import owner
from src.computermanager.brain import NPCBrain
from src.objectmanager.objects.pawn import pawn

class npc(owner):
    """
    A non player controllable 'owner'
    """

    def __init__(self, id, name, color: str, conversion, boardmanager) -> None:
        super().__init__(id, name, color)
        self.control = "auto"
        self.brain = NPCBrain(self, conversion, boardmanager)
    
    def decide(self, unit: pawn):
        """
        Get a decision from the npc.
        """
        if unit.health > 2:
            return self.brain.findTargetDirection(unit, "event")
        if unit.health <= 2 and len(self.units) > 1:
            return self.brain.runTo(unit, "event")
        else:
            return self.brain.findTargetDirection(unit, "event")