from src.conversion import convert_coords
from gamemanager.board import boardManager
from gamemanager.units import unitController
from gamemanager.players.owners import owner
import time

class NPCBrain:
    def __init__(self, owner: owner, conversion: convert_coords, mang:  boardManager) -> None:
        self.conversion = conversion
        self.mang = mang
        self.owner = owner

    def runTo(self, unit, returnformat) -> list:
        return [self.conversion.convert_action_str_to_position_event(unit, \
            unitController.coord_to_action_str(unit, unitController.get_first_walkable(unit, self.mang))), "move"]

    def findTargetDirection(self, unit, returnformat) -> list:
        """
        1. search the board for targets above or below.
        2. move in that direction
        
        """
        time.sleep(0.2)
        pawns = self.mang.get_all_pawns(self.mang.board)
        options = []
        for i in pawns:
            if i.owner != self.owner:
                dist = unitController.count(unit, i.loc)
                options.append({"unit":i, "direction": unitController.is_above_or_below_right_or_left(unit, i.loc, self.mang), "distance": dist})

        if len(options) > 0:
            closest = min(options, key=lambda x:x['distance'])
        else:
            return ["", "winner"]
        
        print(f"closest target: {closest}")

        def checkMove():
            if closest["distance"] == 1:
                return "attack"
            else:
                return "move"

        if checkMove() == "attack":
            targetUnit = self.mang.get_adjacent_enemy(unit.loc, self.owner)
            print(f"target unit: {targetUnit}")
            if returnformat == "event" and targetUnit != None: #convert_map_to_position_event
                return [self.conversion.convert_map_to_position_event(targetUnit.loc), checkMove()]
  
        if returnformat == "event":
            return [self.conversion.convert_action_str_to_position_event(unit, closest["direction"]), checkMove()]
        

    