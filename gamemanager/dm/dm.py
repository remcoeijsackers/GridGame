# Game state monitoring
from gamemanager.players.owners import owner

class gameController:
    """
    Handles game state monitoring.
    """
    def __init__(self, first_player, second_player, computer) -> None:
        self.first_player : owner = second_player
        self.second_player: owner = first_player
        self.computer: owner = computer
        self.turnOrder = ["p1","p2", "computer"]
        self.openSlots = [self.first_player, self.second_player, self.computer]
        self.closedSlots = []
        self.current_player = self.first_player

    def __getNextPlayer(self, current):
        if len(self.openSlots) > 0:
            nextplayer = dict(self.openSlots, key=lambda x:x['openTurn'])
            if nextplayer:
                return nextplayer
                
    def action_or_switch(self):

        if self.current_player.available_actions == 2:
            print(self.current_player.startTurn())

        if self.current_player.available_actions >= 1:
            self.current_player.action()

        else: 
            self.current_player.available_actions = 2
            self.openSlots.remove(self.current_player)
            self.closedSlots.append(self.current_player)
            tmp = self.current_owner
            self.current_owner = self.other_owner
            self.other_owner = tmp

        return self.current_owner

    def switch_player(self):
        self.current_owner.available_actions = 2
        tmp = self.current_owner
        self.current_owner = self.other_owner
        self.other_owner = tmp
        return self.current_owner

    def check_game_state(self):
        all_units_owner1 = len(self.current_owner.units)
        x = 0

        for i in self.current_owner.units:
            if i.destroyed == True:
                x += 1
        
        if all_units_owner1 == x:
            return self.other_owner

        all_units_owner2 = len(self.other_owner.units)
        x = 0

        for i in self.other_owner.units:
            if i.destroyed == True:
                x += 1
        if all_units_owner2 == x:
            return self.current_owner
        