import time

from src.conversion.conversion import convert_coords
from src.gamemanager.board import boardManager
from src.gamemanager.units import unitController
from src.gamemanager.players.owners import owner
from src.gamemanager.settings import debug

class NPCBrain:
    def __init__(self, owner: owner, conversion: convert_coords, mang:  boardManager) -> None:
        self.conversion = conversion
        self.mang = mang
        self.owner = owner
        self.target = None

    def runTo(self, unit, returnformat) -> list:
        """
        move a selected unit to a random 'save' location.
        """
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
            if self.target == None:
                closest = min(options, key=lambda x:x['distance'])
                self.target = closest["unit"]
            else:
                if self.target.health > 0:
                    dist = unitController.count(unit, self.target.loc)
                    closest = {"unit":self.target, "direction": unitController.is_above_or_below_right_or_left(unit, self.target.loc, self.mang), "distance": dist}
                else:
                    closest = min(options, key=lambda x:x['distance'])
                    self.target = closest["unit"]


        else:
            return ["", "winner"]
        if debug:
            print(f"{self.owner} npc: closest target: {closest}")

        def checkMove():
            if closest["distance"] == 1:
                return "attack"
            else:
                return "move"

        if checkMove() == "attack":
            targetUnit = self.mang.get_adjacent_enemy(unit.loc, self.owner)
            if debug:
                print(f"{self.owner} npc: target unit: {targetUnit}")
            if returnformat == "event" and targetUnit != None: #convert_map_to_position_event
                return [self.conversion.convert_map_to_position_event(targetUnit.loc), checkMove()]
  
        if returnformat == "event":
            return [self.conversion.convert_action_str_to_position_event(unit, closest["direction"]), checkMove()]
        

    