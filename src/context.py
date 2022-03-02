
class modal_context:
    def __init__(self, title, options, ctype, command) -> None:
        self.title: str = title
        self.options: str = options
        self.type: str = ctype
        self.command: function = command
