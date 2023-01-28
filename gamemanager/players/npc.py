from gamemanager.players.owners import owner
from computermanager.brain import NPCBrain

class npc(owner):

    def __init__(self, id, name, color: str, conversion, boardmanager) -> None:
        super().__init__(id, name, color)
        self.control = "auto"
        self.brain = NPCBrain(self, conversion, boardmanager)
    
    def decide(self, unit):
        """
        Get a decision from the npc
        """
        return self.brain.findTargetDirection(unit, "event")