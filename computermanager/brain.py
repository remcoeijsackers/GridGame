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

    def findTargetDirection(self, unit, returnformat) -> list:
        """
        1. search the board for targets above or below.
        2. move in that direction
        
        """
        pawns = self.mang.get_all_pawns(self.mang.board)
        options = []
        for i in pawns:
            if i.owner != self.owner:
                dist = unitController.count(unit, i.loc)
                options.append({"unit":i, "direction": unitController.is_above_or_below_right_or_left(unit, i.loc), "distance": dist})

        closest = min(options, key=lambda x:x['distance'])
        print(f"closest target: {closest}")

        def getAction():
            if closest["direction"] == "above":
                return "up"
            if closest["direction"] == "below":
                return "down"
            if closest["direction"] == "right":
                return "right"
            if closest["direction"] == "left":
                return "left"

        def checkMove():
            if closest["distance"] == 1:
                return "attack"
            else:
                return "move"

        if checkMove() == "attack":
            targetUnit = self.mang.get_adjacent_enemy(unit.loc, 1, self.owner)
            print(f"target unit: {targetUnit}")
            if returnformat == "event" and targetUnit != None:
                return [self.conversion.convert_map_to_position_event(targetUnit.loc), checkMove()]

        if returnformat == "logical":
            return [self.conversion.convert_action_str_to_logical(unit, getAction()), checkMove()]
        if returnformat == "grid":
            return [self.conversion.convert_action_str_to_grid_position(unit, getAction()), checkMove()]
        if returnformat == "event":
            return [self.conversion.convert_action_str_to_position_event(unit, getAction()), checkMove()]
        

    