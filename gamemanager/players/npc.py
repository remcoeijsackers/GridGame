from gamemanager.players.owners import owner
from computermanager.brain import NPCBrain
from objectmanager.objects.pawn import pawn

class npc(owner):

    def __init__(self, id, name, color: str, conversion, boardmanager) -> None:
        super().__init__(id, name, color)
        self.control = "auto"
        self.brain = NPCBrain(self, conversion, boardmanager)
    
    def decide(self, unit: pawn):
        """
        Get a decision from the npc
        """
        if unit.health >= 2:
            return self.brain.findTargetDirection(unit, "event")
        else:
            return self.brain.runTo(unit, "event")