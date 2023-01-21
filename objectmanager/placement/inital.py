from src.unitgen import unitgenerator
from src.manager import manager, unitcontroller, placement
from src.util import placeip, placeipRigid
from src.state import state
from src.objects import broken_cell, cell, scenery, pawn, building, enemy, water, tree
from src.grid import grid
from src.settings import debug, gridsize, symbolsize
from src.conversion import convert_coords
from src.controller import controller, owner
from src.context import modal_context, settings_context, color_context, unit_modal_context,placement_context
from src.ui import uihandler, painter

from objectmanager import generator
def create_pieces(parent, player_one, player_two, settings: settings_context, brd,  placement: placement_context ):

        for i in range(settings.var_trees):
            makore = tree("T")
            placeip(brd.board, makore)
        
        for i in range(settings.var_water_clusters):
            water_clustr = water("W")
            brd.placeclus(water_clustr)

        for i in range(settings.var_units1):
            soldier = pawn("P1-{}".format(i))
            soldier.fullname = generator.unitgenerator.get_name()
            soldier.owner = player_one
            soldier.set_image(generator.unitgenerator.get_image())
            soldier.set_age(generator.unitgenerator.get_age())
            player_one.units.append(soldier)
            if parent.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "top")

        for i in range(settings.var_units2):
            soldier = pawn("P2-{}".format(i))
            soldier.fullname = generator.unitgenerator.get_name()
            soldier.owner = player_two
            soldier.set_image(generator.unitgenerator.get_image())
            soldier.set_age(generator.unitgenerator.get_age())
            player_two.units.append(soldier)
            if parent.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "bottom")
        
        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

        for i in range(settings.var_npcs):
            npc = enemy("NPC")
            npc.fullname = generator.unitgenerator.get_name()
            npc.set_image(generator.unitgenerator.get_image())
            npc.set_age(generator.unitgenerator.get_age())
            placeip(brd.board, npc)
 