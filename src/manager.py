import pandas as pd
import random
from pandas.core.frame import DataFrame

from src.util import fullcols, placeip, colsandrows, placeip_near_wall, colsc, colsr
from src.objects import cell, unit, player, scenery, building, broken_cell
from src.settings import gridsize, debug

from src.controller import owner

class placement:
    """
    Handles seed generation, random placement of units
    """
    def __init__(self, seed):
        self.seed = seed
        self.coreseed = seed[:len(seed)//2]
        self.subseed = seed[len(seed)//2:]

    def placeip(self, board, placee):
        for i,x in list(zip(self.coreseed, self.subseed)):
            def cl():
                random.seed(int(i))
                return random.choice(fullcols[:gridsize])
            def rc():
                random.seed(int(x))
                return random.choice(range(gridsize))
            r = rc()
            c = cl()
            if hasattr(board.at[r, c], 'walkable'):
                board.at[r, c] = placee
            else: 
                placeip(board, placee)
            placee.set_loc((r,c))
            if debug:
                print(r,c)
        return r, c

    def generate(self, board):
        #placing units
        pla = [unit(i) for i in ["E", "E"]]
        [self.placeip(self.board, i) for i in pla]

        #placing obstacles
        random.seed(int(self.coreseed))
        plb = [building(i) for i in ["B" for i in range(random.randint(1,6))]]
        [self.placeip(board, i) for i in plb] 

        #placing scenery
        random.seed(int(self.subseed))
        pls = [scenery(i) for i in ["T" for i in range(random.randint(1,6))]]
        [self.placeip(board, i) for i in pls]  
        return board

class manager:
    def show(self) -> DataFrame:
        return self.board
    
    def set_board(self, board: DataFrame) -> None:
        self.board = board 

    def inspect(self, loc):
        pr = colsc().get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        return contents

    def explain(self, loc):
        pr = colsc().get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        return contents.description
    
    def search(self, item):
        """
        loop trough the entire dataframe until there is a match on name, then return the location
        """
        for loclist in colsandrows():
            for loc in loclist:
                pr = colsc().get(loc[1])
                contents = self.board.iloc[int(loc[0])][int(pr)]
                if item == str(contents):
                    return loc
                    
    def gethealth(self, loc):
        pr = colsc().get(loc[1])
        contents = self.board.iloc[int(loc[0])][int(pr)]
        if hasattr(contents, 'health'):
            return str(contents.health)
        else: 
            return ""
    
    def broken_tiles(self, board: DataFrame):
        for spot in colsandrows():
            for coord in spot:
                if isinstance(board.at[coord[0], coord[1]], broken_cell):
                    broken_cell.loc = coord
                    yield coord

    def iter_coords(self):
        """
        Return all coordinates in the board.
        """
        for spot in colsandrows():
            for coord in spot:
                yield coord

    def give_all_cells_coords(self):
        """
        Give all cells a loc
        """
        for spot in colsandrows():
            for coord in spot:
                cl = self.inspect(coord)
                if isinstance(cl, cell):
                    cl.set_loc(coord)
                
    def get_all_cells(self, board: DataFrame):
        """
        Return all coordinates in the board.
        """
        self.give_all_cells_coords()
        all_items_on_board = board.to_numpy()
        for row in all_items_on_board:
            for item in row:
                if isinstance(item, cell) and item.stepped_on > 0:
                    yield item
                    
    def get_all_clean_cells(self, board: DataFrame):
        """
        Return all coordinates in the board.
        """
        self.give_all_cells_coords()
        all_items_on_board = board.to_numpy()
        for row in all_items_on_board:
            for item in row:
                if isinstance(item, cell):
                    yield item

    def get_adjacent_cells(self, loc, distance):
        """
        check if something is adjacent to something else, in a square grid (including vertical)
        """
        def __count(mainloc, otherloc) -> int:
            z = mainloc[0], colsc().get(mainloc[1])
            b = int(otherloc[0]), colsc().get(otherloc[1])
            outcome = abs(z[0] - b[0]) + abs(z[1] - b[1])
            return outcome

        for i in self.iter_coords():
            if __count(loc, i) <= distance:
                yield i

    def get_right_and_left_cells(self, coord):
        """
        get the type of cell right and left
        """
        def __check(coord):
            left = coord[0], colsr().get(colsc().get(coord[1])  - 1)
            right = int(coord[0]), colsr().get(colsc().get(coord[1]) + 1)
            return left, right

        return __check(coord)

    def get_top_and_bottom_cells(self, coord):
        """
        get the type of cell right and left
        """
        def __check(coord):
            top = coord[0] -1, coord[1]
            bottom = int(coord[0]) +1, coord[1]
            return top, bottom

        return __check(coord)

    def is_on_same_row(self, unitloc0, itemloc0):
        """
        check if something is on the same row with something else.
        """
        if unitloc0 == itemloc0:
            return True
        else:
            return False

    def is_on_same_col(self, unitloc1, itemloc1):
        """
        check if something is on the same column with something else.
        """
        if unitloc1 == itemloc1:
            return True
        else:
            return False

    def get_all_objects(self, board: DataFrame):
        """
        Get all (non cell) objects in the dataframe.
        """
        all_items_on_board = board.to_numpy()
        for row in all_items_on_board:
            for item in row:
                if not isinstance(item, cell):
                    yield item
    
    def get_coords_of_all_objects(self, board: DataFrame):
        """
        Get the coordinates all (non cell) objects in the dataframe.
        """
        all_items_on_board = board.to_numpy()
        for row in all_items_on_board:
            for item in row:
                if not isinstance(item, cell):
                    yield item.loc

    def get_items_in_row(self, board: DataFrame, row: int):
        """
        Get all items in a row in the dataframe.
        """
        all_items_in_row = board.iloc[row]
        for item in all_items_in_row:
            if not isinstance(item, cell):
                yield item

    def get_items_in_col(self, board: DataFrame, col: str):
        """
        Get all items in a column in the dataframe.
        """
        all_items_in_col = board[col]
        for item in all_items_in_col:
            if not isinstance(item, cell):
                yield item
    
    def get_coords_of_items_in_row(self, board: DataFrame, row: int):
        """
        Get the coordinates of all items in a row in the dataframe.
        """
        all_items_in_row = board.iloc[row]
        for item in all_items_in_row:
            if not isinstance(item, cell):
                yield item.loc

    def get_coords_of_items_in_col(self, board: DataFrame, col: str):
        """
        Get the coordinates of all items in a column in the dataframe.
        """
        all_items_in_col = board[col]
        for item in all_items_in_col:
            if not isinstance(item, cell):
                yield item.loc
    
    def get_coords_of_items_in_diagonal_topleft_to_bottomright(self, board: DataFrame, unit):
        """
        Get the coordinates of all items in a diagonal row in the dataframe.
        """
        temploc = unit.loc
        tt = temploc[0]
        newloc0 = temploc[0]
        newloc1 = colsc().get(temploc[1]) 
        locs = []
        # check from unit to topleft
        while tt > 0:

            newloc0 -= 1 
            newloc1 -= 1

            colcheck = colsr().get(newloc1)
            if colcheck == 'A' or colcheck == None:
                break
            clcheck = board.iloc[int(newloc0)][int(colsc().get(colcheck))]
            if not isinstance(clcheck.__class__, cell):
                locs.append((newloc0, '{}'.format(colcheck)))
            tt -= 1
        tt = unit.loc[0]
        newloc0 = temploc[0]
        newloc1 = colsc().get(temploc[1]) 
        # check from unit to bottomright
        while tt < 9:
            newloc0 += 1 
            newloc1 += 1
            colcheck = colsr().get(newloc1)
            if colcheck == fullcols[:gridsize][-1] or colcheck == None:
                break

            clcheck = board.iloc[int(newloc0)][int(colsc().get(colcheck))]

            if not isinstance(clcheck.__class__, cell):
                locs.append((newloc0, '{}'.format(colcheck)))
            tt += 1
        for coord in locs:
            yield coord

    def get_coords_of_items_in_diagonal_topright_to_bottomleft(self, board: DataFrame, unit):
        """
        Get the coordinates of all items in a diagonal row in the dataframe.
        """
        temploc = unit.loc
        tt = temploc[0]
        newloc0 = temploc[0]
        newloc1 = colsc().get(temploc[1]) 
        locs = []
        while tt > 0:
            newloc0 -= 1 
            newloc1 -= 1
            colcheck = colsr().get(newloc1)
            if colcheck == fullcols[:gridsize][-1] or colcheck == None:
                break

            clcheck = board.iloc[int(newloc0)][int(colsc().get(colcheck))]
            if not isinstance(clcheck.__class__, cell):
                locs.append((newloc0, '{}'.format(colcheck)))
            tt -= 1
        tt = unit.loc[0]
        newloc0 = temploc[0]
        newloc1 = colsc().get(temploc[1]) 
        while tt < 9:
            newloc0 += 1 
            newloc1 += 1
            colcheck = colsr().get(newloc1)
            if colcheck == 'A' or colcheck == None:
                break

            clcheck = board.iloc[int(newloc0)][int(colsc().get(colcheck))]

            if not isinstance(clcheck.__class__, cell):
                locs.append((newloc0, '{}'.format(colcheck)))
            tt += 1
        for coord in locs:
            yield coord
            
    def block_walk_behind_object_in_row(self, board: DataFrame, unit):
        """
        Get the coordinates of cells after items in a row in the dataframe.
        """
        for i in self.get_coords_of_items_in_row(board, unit.loc[0]):
            col_unit = colsc().get(unit.loc[1])
            col_object = colsc().get(i[1])
            if not isinstance(i, player):
                if col_unit < col_object:
                    # + if object is to the right of player
                    if i[1] != 'J': 
                        x = col_object + 1
                        yield (i[0], colsr().get(x))

                elif col_unit > col_object:
                    # - if object is to the left of player
                    if i[1] != 'A': 
                        x = col_object - 1
                        yield (i[0], colsr().get(x))

    def block_walk_behind_object_in_col(self, board: DataFrame, unit):
        """
        Get the coordinates of cells after items in a column in the dataframe.
        """
        for i in self.get_coords_of_items_in_col(board, unit.loc[1]):
            row_unit = unit.loc[0]
            row_object = i[0]
            if not isinstance(i, player):
                if row_unit < row_object:
                    # + if object is below player
                    if i[0] != 9: 
                        x = row_object + 1
                        z = (x, i[1])
                        yield z

                elif row_unit > row_object:
                    # - if object is above player
                    if i[0] != 0: 
                        x = row_object - 1
                        z = (x, i[1])
                        yield z

    def placeclus(self, placee):
        """
        Place a cluster around an object.
        Creates new instances of the objects class.
        """
        classfromobject = placee.__class__
        name = placee.name
        placeip_near_wall(self.board, placee)
        for i in self.get_adjacent_cells(placee.loc, 2):
            x = classfromobject(name)
            self.board.at[i[0], i[1]] = x
            x.set_loc((i[0], i[1]))

class unitcontroller:
    def count(self, unit, loc) -> int:
        """
        Count how many steps an action would take.
        """
        z = unit.loc[0], colsc().get(unit.loc[1])
        b = int(loc[0]), colsc().get(loc[1])
        # for singular vertical moves
        if abs(z[0] - b[0]) ==  1 and abs(z[1] - b[1]) == 1:
            # both are one
            outcome = 1
        elif (abs(z[0] - b[0]) !=  1 and abs(z[1] - b[1]) != 1) and abs(z[0] - b[0]) == abs(z[1] - b[1]):
            #both are the same, but not one
            outcome = abs(z[0] - b[0])

        else: 
            outcome = abs(z[0] - b[0]) + abs(z[1] - b[1])
        return outcome
    
    def sub_possible_moves(self, unit, boardmanager: manager, total=False, turns=1):
        """
        Return the coordinates an unit can walk to.
        """
        filter_coords = []
        for i in boardmanager.block_walk_behind_object_in_row(boardmanager.board, unit):
            filter_coords.append(i)
        for i in boardmanager.block_walk_behind_object_in_col(boardmanager.board, unit):
            filter_coords.append(i)
        #for i in boardmanager.get_coords_of_items_in_diagonal_topleft_to_bottomright(boardmanager.board, unit):
        #    filter_coords.append(i)
        #for i in boardmanager.get_coords_of_items_in_diagonal_topright_to_bottomleft(boardmanager.board, unit):
        #    filter_coords.append(i)
        for spot in colsandrows():
            for coord in spot:
                if not total:
                    if self.count(unit, coord) <= unit.range and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                        yield coord
                else: 
                    if turns > 0:
                        if self.count(unit, coord) <= unit.range * (turns + 1) and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                            yield coord
                    else:
                        if self.count(unit, coord) <= unit.range * turns  and getattr(boardmanager.board.at[coord[0], coord[1]], 'walkable') and coord not in filter_coords:
                            yield coord


    def possible_moves(self, unit, boardmanager: manager, total=False, turns=1):
        tmpcords = []
        retcords = []
        movecords = []

        for spot in colsandrows():
            for coord in spot:
                tmpcords.append(coord)
        
        for coord in self.sub_possible_moves(unit, boardmanager, total, turns):
            movecords.append(coord)

        for i in tmpcords:
            subcords = []
            topsubcords = []
            for crd in boardmanager.get_right_and_left_cells(i):
                subcords.append(crd)
            for crd in boardmanager.get_top_and_bottom_cells(i):
                topsubcords.append(crd)

            if subcords[0] in movecords and subcords[1] in movecords and not i == unit.loc:
                retcords.append(i)
            if topsubcords[0] in movecords and topsubcords[1] in movecords and not i == unit.loc: 
                retcords.append(i)
            subcords = []
            topsubcords = []
        
        for i in movecords:
            retcords.append(i)

        for i in retcords:
            yield i

        retcords = []
        movecords = []
    
    def possible_melee_moves(self, selected_unit, board: DataFrame, controlling_player: owner):
        """
        Return the coordinates an unit can attack.
        """
        for spot in colsandrows():
            for coord in spot:
                # check if its a cell
                if self.count(selected_unit, coord) <= selected_unit.melee_range and getattr(board.at[coord[0], coord[1]], 'walkable'):
                    yield coord
                else:
                    # if its not a cell, but a piece of scenery or a unit, melee is posible
                    if coord != selected_unit.loc:
                        if self.count(selected_unit, coord) <= selected_unit.melee_range and (isinstance(board.at[coord[0], coord[1]], scenery) or isinstance(board.at[coord[0], coord[1]], unit) or isinstance(board.at[coord[0], coord[1]], building) and not board.at[coord[0], coord[1]] in controlling_player.units):
                            yield coord

    def place(self, unit: unit, loc, boardmanager: manager) -> DataFrame and bool:
        """
        Place an unit to another spot in the dataframe.
        """
        pr = colsc().get(loc[1])
        ul = colsc().get(unit.loc[1])
        if getattr(boardmanager.board.at[loc[0], loc[1]], 'walkable') and loc in self.possible_moves(unit, boardmanager):
            newboard = boardmanager.board
            newboard.iloc[int(unit.loc[0])][int(ul)] = cell(stepped_on=1) 
            newboard.iloc[int(loc[0])][int(pr)] = unit 
            unit.set_loc((int(loc[0]),loc[1]))
            return newboard, True
        else:
            return boardmanager.board, False


    def attack(self, loc, board, damage) -> DataFrame:
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
            if isinstance(board.iloc[int(loc[0])][int(pr)], unit):
                attacked_unit: unit = board.iloc[int(loc[0])][int(pr)]
                attacked_unit.take_damage(damage)
        return board

    def attack_on_loc(self, loc, board):
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

class unitbrain:
    def __init__(self) -> None:
        pass

    