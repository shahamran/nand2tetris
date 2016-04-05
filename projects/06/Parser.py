import os
from Command import Command

""" The parser module for the assembler.
"""

# Constants.
COMMENT_PREFIX = '//'
READ_ONLY = 'r'
DEF_ENCODING = 'utf-8'
EMPTY_LINE = ''
A_COMMAND_PREFIX = '@'
L_COMMAND_PREFIX = '('
content = []

def parse(file_name):
    """ Parse a given assembly language file.
    """
    # Clean up when parsing a new file
    global content
    content = []
    current_command = None
    # Read the file and parse lines
    with open(file_name, mode=READ_ONLY, encoding=DEF_ENCODING) as asm_file:
        for line in asm_file:
            # Ignore whitespace & comments in the start and end of the line
            found_comment = line.find(COMMENT_PREFIX)
            if found_comment != -1:
                line = line[:found_comment]

            line = line.replace(" ", "").strip()
            if line.isspace() or line == EMPTY_LINE:
                continue
            # Determine whether current line is A/L/C Command (L for Label)
            elif line.startswith(A_COMMAND_PREFIX):
                current_command = Command(Command.A_COMMAND, line[1:])
            elif line.startswith(L_COMMAND_PREFIX):
                current_command = Command(Command.L_COMMAND, line[1:-1])
            else:
                current_command = Command(Command.C_COMMAND, line)

            # Add the created command to the content list
            content.append(current_command)

        # For loop ends here.

    # File is closed here

def get_commands():
    """ Get all commands in a parsed file - use this after running the parse function.
    This is a generator, thus running 'for command in get_commands()' will yield
    all commands in the parsed file in the correct order.
    """
    for command in content:
        yield command
