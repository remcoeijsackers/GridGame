from objectmanager.placement.functions import placeip, placementHandler, placeclus

from objectmanager.objects.scenery import  building, water, tree

from contexts.settingscontext import settings_context, placement_context, placement_details_context

from objectmanager.objects.pawn import pawn

from objectmanager import generator


from gamemanager.players.owners import owner
from gamemanager.players.npc import npc


def create_pieces(parent, players: (owner), settings: settings_context, brd,  placement: placement_context ):

    def handle_placement(brd, obj, mode, compass=None, detail=None, specific=False):
        details_context = placement_details_context(mode, compass, detail, specific=specific)
        return placementHandler(brd.board, obj, details_context)

    for i in range(settings.var_trees):
        makore = tree("T")
        handle_placement(brd, makore, "fuzzy")
    
    for i in range(settings.var_water_clusters):
        water_clustr = water("W")
        placeclus(brd, water_clustr)

    bottomUsed = False
    topUsed = False
    leftUsed = False
    rightUsed = False
    for player in players:
        for i in range(settings.var_units):
            soldier = pawn("{}-{}".format(i, player.id),generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), player)
            player.units.append(soldier)
        
    for player in players:
        for unit in player.units:
            #if isinstance(player, npc):
            #    handle_placement(brd, unit, "fuzzy")
                
            if bottomUsed == False:
                bottomUsed = True
                handle_placement(brd, unit, "rigid", "bottom", "center",True)
                    
            if topUsed == False:
                topUsed = True
                handle_placement(brd, unit, "rigid", "top", "center",True)
                    
            if leftUsed == False:
                leftUsed = True
                handle_placement(brd, unit, "rigid", "bottom", "center",True)

            if rightUsed == False:
                rightUsed = True
                handle_placement(brd, unit, "rigid", "bottom", "center",True)

            else:
                handle_placement(brd, unit, "fuzzy")
        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

