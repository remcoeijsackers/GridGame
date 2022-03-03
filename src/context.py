
class modal_context:
    def __init__(self, title, description, ctype, command=None) -> None:
        self.title: str = title
        self.description: str = description
        self.ctype: str = ctype
        self.command: function = command
