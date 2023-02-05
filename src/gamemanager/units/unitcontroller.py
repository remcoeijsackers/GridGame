from pandas.core.frame import DataFrame
import math

from util.util import colsandrows, colsc, getCoordLine, topL, topR, bottomL, bottomR, top, left, right, bottom
from src.objectmanager.objects.grid import cell
from src.objectmanager.objects.scenery import scenery, building
from src.objectmanager.objects.grid import broken_cell
from src.objectmanager.objects.pawn import pawn
from src.gamemanager.players.owners import owner
from src.gamemanager.board import boardManager



def calculate_distance( unit, loc) -> int:
    x1 = unit.loc[0]
    y1 = colsc().get(unit.loc[1])
    x2 = loc[0]
    y2 = colsc().get(loc[1])
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    mind = min(dx, dy)
    maxd = max(dx, dy)
    diagstep = mind
    straigthstep = maxd - mind
    return round(math.sqrt(2) * diagstep + straigthstep)

def count( unit, loc) -> int:
    """
    Count how many steps an action would take.
    """
    return calculate_distance(unit, loc)

def coord_to_action_str(unit, coord):
    """
    Translate a a location and a unit into a action string for movement.
    """
    if is_above_me(unit, coord):
        return "top"
    if  is_below_me(unit, coord):
        return "bottom"
    if is_left_me(unit, coord):
        return "left"
    if is_right_me(unit, coord):
        return "right"
    if topL(unit.loc) == coord:
        return "topleft"
    if topR(unit.loc) == coord:
        return "topright"
    if bottomL(unit.loc) == coord:
        return "bottomleft"
    if bottomR(unit.loc) == coord:
        return "bottomRight"

def is_above_or_below_right_or_left(unit, loc, brd):
        """
        Get whether a location is (generally) above, below, a unit
        If the loc falls in line with the units loc, get a specific: left, right, topleft, topright, bottomleft, bottomright.
        """

        action = "move"

        if count(unit, loc) == 1:
            action = "attack"

        if check_for_enemy_in_coordslist(unit, getCoordLine(unit.loc, ["topleft"]), brd):
            if action == "move":
                if is_walkable(topL(unit.loc), brd):
                    return "topleft"
            else:
                return "topleft"

        if check_for_enemy_in_coordslist(unit, getCoordLine(unit.loc, ["topright"]), brd):
            if action == "move":
                if is_walkable(topR(unit.loc), brd):
                    return "topright"
            else:
                return "topright"

        if check_for_enemy_in_coordslist(unit, getCoordLine(unit.loc, ["bottomleft"]), brd):
            if action == "move":
                if is_walkable(bottomL(unit.loc), brd):
                    return "bottomleft"
            else:
                return "bottomleft"

        if check_for_enemy_in_coordslist(unit, getCoordLine(unit.loc, ["bottomright"]), brd):
            if action == "move":
                if is_walkable(bottomR(unit.loc), brd):
                    return "bottomright"
            else:
                return "bottomright"

        if  is_above_me(unit, loc):
            if action == "move":
                if is_walkable(top(unit.loc), brd):
                    return "top"
            else:
                return "top"

        if  is_below_me(unit, loc):
            if action == "move":
                if is_walkable(bottom(unit.loc), brd):
                    return "bottom"
            else:
                return "bottom"

        if is_left_me(unit, loc):
            if action == "move":
                if is_walkable(left(unit.loc), brd):
                    return "left"
            else:
                return "left"

        if is_right_me(unit,loc):
            if action == "move":
                if is_walkable(right(unit.loc), brd):
                    return "right"
            else: 
                return "right"
        
        if action == "move":
            return coord_to_action_str(unit, get_first_walkable(unit, brd))

def check_for_enemy_in_coordslist(unit, coords, brd):
    for i in coords:
        if isinstance(brd.inspect(i), pawn):
            if brd.inspect(i).owner != unit.owner:
                return True
    return False

def check_for_object_in_coordlist(coords, objectclass, brd):
    for i in coords:
        if isinstance(brd.inspect(i.loc), objectclass):
            return True
    return False

def is_walkable(loc, brd) -> bool:
    if brd.inspect(loc).walkable == True:
        return True
    return False

def get_first_walkable(unit, brd):
    for i in brd.get_adjacent_cells(unit.loc, 1):
        if brd.inspect(i).walkable == True:
            return i

def is_above_me( unit, loc) -> bool:
        """
        Check if a loc is above the unit
        """
        if unit.loc[0] > loc[0]:
            return True
        else: 
            return False

def is_below_me( unit, loc) -> bool:
        """
        Check if a loc is above the unit
        """
        if unit.loc[0] < loc[0]:
            return True
        else: 
            return False

def is_left_me( unit, loc) -> bool:
        """
        Check if a loc is left from the unit
        """
        if colsc().get(loc[1]) < colsc().get(unit.loc[1]):
            return True
        else: 
            return False

def is_right_me( unit, loc) -> bool:
        """
        Check if a loc is right from the unit
        """
        if colsc().get(loc[1]) > colsc().get(unit.loc[1]):
            return True
        else: 
            return False

def sub_possible_moves( unit, boardmanager: boardManager, total=False, turns=0):
        """
        Return the coordinates an unit can walk to.
        """
        filter_coords = []
        for i in boardmanager.block_walk_behind_object_in_row(boardmanager.board, unit):
            filter_coords.append(i)
        for i in boardmanager.block_walk_behind_object_in_col(boardmanager.board, unit):
            filter_coords.append(i)
        for spot in colsandrows():
            for coord in spot:
                if not total:

                    if  count(unit, coord) <= unit.range and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                        yield coord
                else:                    
                    if turns > 0:
                        if  count(unit, coord) <= unit.range * turns and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                            yield coord
                    else:
                        if  count(unit, coord) <= unit.range  and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                            yield coord


def possible_moves( unit, boardmanager: boardManager, total=False, turns=1):
        tmpcords = []
        retcords = []
        movecords = []

        for spot in colsandrows():
            for coord in spot:
                tmpcords.append(coord)
        
        for coord in  sub_possible_moves(unit, boardmanager, total, turns):
            movecords.append(coord)
                    
        for i in movecords:
            retcords.append(i)

        for i in retcords:
            yield i

        retcords = []
        movecords = []
    
def possible_melee_moves( selected_unit, board: DataFrame, controlling_player: owner):
        """
        Return the coordinates an unit can attack.
        """
        for spot in colsandrows():
            for coord in spot:
                # check if its a cell
                if  count(selected_unit, coord) <= selected_unit.melee_range and getattr(board.at[coord[0], coord[1]], 'walkable'):
                    yield coord
                else:
                    # if its not a cell, but a piece of scenery or a unit, melee is posible
                    if coord != selected_unit.loc:
                        if  count(selected_unit, coord) <= selected_unit.melee_range and (isinstance(board.at[coord[0], coord[1]], scenery) or isinstance(board.at[coord[0], coord[1]], pawn) or isinstance(board.at[coord[0], coord[1]], building) and not board.at[coord[0], coord[1]] in controlling_player.units):
                            yield coord

def possible_ranged_moves( selected_unit, board: DataFrame, controlling_player: owner):
        """
        Return the coordinates an unit can attack.
        """
        for spot in colsandrows():
            for coord in spot:
                # check if its a cell
                if  count(selected_unit, coord) <= selected_unit.melee_range and getattr(board.at[coord[0], coord[1]], 'walkable'):
                    yield coord
                else:
                    # if its not a cell, but a piece of scenery or a unit, melee is posible
                    if coord != selected_unit.loc:
                        if  count(selected_unit, coord) <= selected_unit.melee_range and (isinstance(board.at[coord[0], coord[1]], scenery) or isinstance(board.at[coord[0], coord[1]], pawn) or isinstance(board.at[coord[0], coord[1]], building) and not board.at[coord[0], coord[1]] in controlling_player.units):
                            yield coord
def place( unit: pawn, loc, boardmanager: boardManager) -> DataFrame and bool:
        """
        Place an unit to another spot in the dataframe.
        """
        pr = colsc().get(loc[1])
        ul = colsc().get(unit.loc[1])
        if getattr(boardmanager.board.at[loc[0], loc[1]], 'walkable') and loc in  possible_moves(unit, boardmanager):
            newboard = boardmanager.board
            newboard.iloc[int(unit.loc[0])][int(ul)] = cell(stepped_on=1) 
            newboard.iloc[int(loc[0])][int(pr)] = unit 
            unit.set_loc((int(loc[0]),loc[1]))
            return newboard, True
        else:
            return boardmanager.board, False


def attack( loc, board, damage) -> DataFrame:
        """
        Attack a cell, scenery or another unit.
        """
        pr = colsc().get(loc[1])
        def __break():
            broken_cell_object = broken_cell()
            board.iloc[int(loc[0])][int(pr)] = broken_cell_object
            broken_cell_object.set_loc(loc)
        def _remove_object():
            object_to_remove = board.iloc[int(loc[0])][int(pr)]
            object_to_remove.destroyed = True
            board.iloc[int(loc[0])][int(pr)] = cell()
            
        if getattr(board.iloc[int(loc[0])][int(pr)], 'walkable'):
            __break()
        else :
            if isinstance(board.iloc[int(loc[0])][int(pr)], scenery):
                _remove_object()
            if isinstance(board.iloc[int(loc[0])][int(pr)], pawn):
                attacked_unit: pawn = board.iloc[int(loc[0])][int(pr)]
                attacked_unit.take_damage(damage)
        return board

def attack_on_loc(loc, board):
        """
        Remote Attack a cell, scenery or another unit.
        """
        pr = colsc().get(loc[1])
        def __break():
            broken_cell_object = broken_cell()
            board.iloc[int(loc[0])][int(pr)] = broken_cell_object
            broken_cell_object.loc = loc
        def _remove_object():
            board.iloc[int(loc[0])][int(pr)] = cell()
            
        if getattr(board.iloc[int(loc[0])][int(pr)], 'walkable'):
            __break()
        else :
            _remove_object()

        return board
