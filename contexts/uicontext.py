class modal_context:
    def __init__(self, title, ctype, command=None) -> None:
        self.title: str = title
        self.ctype: str = ctype
        self.command: function = command

class unit_modal_context(modal_context):
    def __init__(self, title, ctype, unit, command=None) -> None:
        super().__init__(title, ctype, command)
        self.unit = unit

