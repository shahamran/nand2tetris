class Command:
    """This class represents an assembly command."""
    
    # Constants:
    C_COMMAND = "C"
    A_COMMAND = "A"
    L_COMMAND = "L"

    # The type of the command - i.e. L for Label, A for Adrress, C for Command
    type = ''

    # The content of the command - i.e. The label (without the parentheses), the address (without @) or the
    # command.
    content = ''

    def __init__(self, type, content):
        """ Basic Constructor, Initializes the command variables
        Input type - the type of the command (L,A or C)
           content - the command content
        """
        self.type = type
        self.content = content
