from src.objectmanager.placement.functions import placeip, placementHandler, placeclus
from src.objectmanager.objects.scenery import  building, water, tree
from src.objectmanager.objects.pawn import pawn
from src.objectmanager import generator
from src.contexts.settingscontext import settings_context, placement_context, placement_details_context
from src.gamemanager.players.owners import owner


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

