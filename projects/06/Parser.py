import os
from Command import Command

# Some constants.
COMMENT_PREFIX = '//'
READ_ONLY = 'r'
DEF_ENCODING = 'utf-8'
A_COMMAND_PREFIX = '@'
L_COMMAND_PREFIX = '('
content = []

def parse(file_name):
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
            if line.isspace() or line == '':
                continue
            # Determine whether current line is A/L/C Command (L for Label)
            elif line.startswith(A_COMMAND_PREFIX):
                current_command = Command('A', line[1:])
            elif line.startswith(L_COMMAND_PREFIX):
                current_command = Command('L', line[1:-1])
            else:
                current_command = Command('C', line)
            content.append(current_command)

def get_commands():
    for command in content:
        yield command
