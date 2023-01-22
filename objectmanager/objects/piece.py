class boardItem:
    def __init__(self) -> None:
        self.name = ""
        self.walkable = False
        self.description = ""
        self.destroyed = False
        self.events = []
        
    def remove(self) -> None:
        del self
    
    def log_event(self,event):
        self.events.append(event)
