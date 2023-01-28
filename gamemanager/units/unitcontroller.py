from pandas.core.frame import DataFrame

from src.util import colsandrows, colsc

from objectmanager.objects.grid import cell
from objectmanager.objects.scenery import scenery, building
from objectmanager.objects.grid import broken_cell
from objectmanager.objects.pawn import pawn
from gamemanager.players.owners import owner
from gamemanager.board import boardManager

import math

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
    
def is_above_or_below_right_or_left( unit, loc):
        if  is_above_me(unit, loc):
            return "above"
        if  is_below_me(unit, loc):
            return "below"
        if is_left_me(unit, loc):
            return "left"
        if is_right_me(unit,loc):
            return "right"

def is_above_me( unit, loc) -> bool:
        """
        Check if a loc is above the unit
        """
        if loc[0] < unit.loc[0]:
            return True
        else: 
            return False

def is_below_me( unit, loc) -> bool:
        """
        Check if a loc is above the unit
        """
        if loc[0] > unit.loc[0]:
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
            broken_cell_object.loc = loc
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
