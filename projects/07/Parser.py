from enum import Enum
from Command import Command
import os

""" The parser module for the assembler.
"""

# Constants.
COMMENT_PREFIX = '//'
READ_ONLY = 'r'
DEF_ENCODING = 'utf-8'
EMPTY_LINE = ''

STR_ARITHMETIC = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
STR_PUSH = 'push'
STR_POP = 'pop'
STR_LABEL = 'label'
STR_GOTO = 'goto'
STR_IF = 'if'
STR_FUNCTION = 'function'
STR_RETURN = 'return'
STR_CALL = 'call'

class CommandType(Enum):
    ''' Enum for the command type.
    '''
    NO_COMMAND = -1
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8


content = []

def parse(file_name):
    """ Parse a given assembly language file.
    """
    # Clean up when parsing a new file
    global content
    content = []
    current_command = None
    # Read the file and parse lines
    with open(file_name, mode=READ_ONLY, encoding=DEF_ENCODING) as vm_file:
        for line in vm_file:
            # Ignore whitespace & comments in the start and end of the line
            found_comment = line.find(COMMENT_PREFIX)
            if found_comment != -1:
                line = line[:found_comment]

            line = line.strip().split(' ')
            if line[0] == EMPTY_LINE:
                continue
            # Determine whether current line is A/L/C CommandType (L for Label)
            elif line[0] in STR_ARITHMETIC:
                current_command = CommandType.C_ARITHMETIC
            elif line[0] == STR_PUSH:
                current_command = CommandType.C_PUSH
            elif line[0] == STR_POP:
                current_command = CommandType.C_POP
            elif line[0] == STR_LABEL:
                current_command = CommandType.C_LABEL
            elif line[0] == STR_GOTO:
                current_command = CommandType.C_GOTO
            elif line[0] == STR_IF:
                current_command = CommandType.C_IF
            elif line[0] == STR_FUNCTION:
                current_command = CommandType.C_FUNCTION
            elif line[0] == STR_RETURN:
                current_command = CommandType.C_RETURN
            elif line[0] == STR_CALL:
                current_command = CommandType.C_CALL

            # Add the created command to the content list
            content.append(Command(current_command, line))

        # For loop ends here.

    # File is closed here

def get_commands():
    """ Get all commands in a parsed file - use this after running the parse function.
    This is a generator, thus running 'for command in get_commands()' will yield
    all commands in the parsed file in the correct order.
    """
    for command in content:
        yield command
