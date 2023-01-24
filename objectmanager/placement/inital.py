from src.util import placeip, placeipRigid

from src.objects import  building, water, tree

from src.context import settings_context,placement_context

from objectmanager.objects.pawn import pawn, enemy
from objectmanager import generator

from gamemanager.players.owners import owner

def create_pieces(parent, players: (owner), settings: settings_context, brd,  placement: placement_context ):

        for i in range(settings.var_trees):
            makore = tree("T")
            placeip(brd.board, makore)
        
        for i in range(settings.var_water_clusters):
            water_clustr = water("W")
            brd.placeclus(water_clustr)

        for i in range(settings.var_units1):
            soldier = pawn("P1-{}".format(i),generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), players[0])
            players[0].units.append(soldier)
            if parent.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "top")

        for i in range(settings.var_units2):
            soldier = pawn("P2-{}".format(i),generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), players[1])
            players[1].units.append(soldier)
            if parent.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "bottom")
        
        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

        #for i in range(settings.var_npcs):
        #    npc = enemy("NPC",generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), computer)
        #    computer.units.append(npc)
        #    placeip(brd.board, npc)
 