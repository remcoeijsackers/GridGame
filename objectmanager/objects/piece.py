class boardItem:
    def __init__(self) -> None:
        self.name = ""
        self.walkable = False
        self.description = ""
        self.destroyed = False
        self.events = []
        self.owner = None
        
    def remove(self) -> None:
        del self
    
    def log_event(self,event):
        self.events.append(event)

    def set_loc(self, loc):
        self.loc = loc
        return self.loc