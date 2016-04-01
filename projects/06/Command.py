class Command:
    'This class represents an assembly command.'
    # The type of the command - i.e. L for Label, A for Adrress, C for Command
    type = ''
    # The content of the command - i.e. The label (without the parentheses), the address (without @) or the
    # command.
    content = ''

    def __init__(self, type, content):
        """ Constructor...
        """
        self.type = type
        self.content = content
