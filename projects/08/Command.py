class Command:
    """This class represents an assembly command."""
    
    # Constants:
    A_ADD = 'add'
    A_SUB = 'sub'
    A_EQ = 'eq'
    A_LT = 'lt'
    A_GT = 'gt'
    A_NEG = 'neg'
    A_AND = 'and'
    A_OR = 'or'
    A_NOT = 'not'

    # The type of the command
    type = -1

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
