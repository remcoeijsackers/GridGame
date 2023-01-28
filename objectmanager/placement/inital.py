from objectmanager.placement.functions import placeip, placeipRigid

from objectmanager.objects.scenery import  building, water, tree

from contexts.settingscontext import settings_context, placement_context

from objectmanager.objects.pawn import pawn, enemy

from objectmanager import generator


from gamemanager.players.owners import owner
from gamemanager.players.npc import npc


def create_pieces(parent, players: (owner), settings: settings_context, brd,  placement: placement_context ):

        for i in range(settings.var_trees):
            makore = tree("T")
            placeip(brd.board, makore)
        
        for i in range(settings.var_water_clusters):
            water_clustr = water("W")
            brd.placeclus(water_clustr)

        bottomUsed = False
        topUsed = False
        for player in players:
            for i in range(settings.var_units):
                soldier = pawn("{}-{}".format(i, player.id),generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), player)
                player.units.append(soldier)
                if isinstance(player, npc):
                    placeipRigid(brd.board, soldier, "center")
                    continue
                if parent.itemPlacement == "rigid":
                    if bottomUsed == False:
                        #bottomUsed = True
                        placeipRigid(brd.board, soldier, "center")
                        continue
                    if topUsed == False:
                        #topUsed = True
                        #placeipRigid(brd.board, soldier, "top")
                        continue
                    
                

        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

