


class owner:
    def __init__(self, name, color) -> None:
        self.name = name
        self.available_actions = 3
        self.units = []
        self.color = color

    def action(self):
        self.available_actions -= 1


class controller:
    def __init__(self, first_player, second_player) -> None:
        self.other_owner : owner = second_player
        self.current_owner: owner = first_player

    def action_or_switch(self):
        if self.current_owner.available_actions > 0:
            self.current_owner.action()
        else: 
            self.current_owner.available_actions = 3
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
        