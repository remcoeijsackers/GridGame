from objectmanager.placement.functions import placeip, placeipRigid

from objectmanager.objects.scenery import  building, water, tree

from contexts.settingscontext import settings_context, placement_context

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

        for player in players:
            for i in range(settings.var_units):
                soldier = pawn("{}-{}".format(i, player.id),generator.unitgenerator.get_name(),generator.unitgenerator.get_age(),generator.unitgenerator.get_image(), player)
                player.units.append(soldier)
                if parent.itemPlacement == "rigid":
                    placeipRigid(brd.board, soldier, "top")

        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

