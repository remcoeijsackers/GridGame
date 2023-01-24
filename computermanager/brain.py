from src.conversion import convert_coords
from gamemanager.board import boardManager
from gamemanager.units import unitController
from gamemanager.players.owners import owner

class NPCBrain:
    def __init__(self, owner: owner, conversion: convert_coords, mang:  boardManager) -> None:
        self.conversion = conversion
        self.mang = mang
        self.owner = owner

    def findTarget(self):
        """
        1. search the board for targets above or below.
        2. move in that direction
        
        """
        pawns = self.mang.get_all_pawns(self.mang.board)
        options = []
        for i in pawns:
            dist = unitController.count(self.owner.units[0], i.loc)
            options.append({"unit":i, "direction": unitController.is_above_or_below(self.owner.units[0], i.loc), "distance": dist})
        closest = max(options, key=lambda x:x['distance'])

        def getAction():
            if closest["direction"] == "above":
                return "up"
            if closest["direction"] == "below":
                return "down"
            else:
                # ! implement: left and right movement
                return "down"


        self.conversion.convert_action_str_to_logical(self.owner.units[0], getAction())
        

    