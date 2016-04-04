import Parser,Code,sys,os
from SymbolsTable import SymbolsTable
from Command import Command

# Constants:
HACK_SUFF = ".hack"
ASM_SUFF = ".asm"
W_FILE_MODE = "w"
DEF_ENCODING = "utf-8"
ASM_SUFF_LEN = len(ASM_SUFF)

""" The assembler main file.
"""
def parse_asm_file(file_name):
    """ Gets the commands list using the parser and scans it twice
        first time searching for labels, second time uses the code to translate
        the A and C commands to machine code.
        Adds the machine code to a new .hack file
        Input: file_name - the .asm file needed to be translated
        Output: the translated file_name.hack file
    """
    line = 0
    symbols_table = SymbolsTable()
    hack_lines = []
    Parser.parse(file_name)
    # First pass
    for command in Parser.get_commands():
        if command.type == Command.L_COMMAND:
            symbols_table.add_label(command.content, line)
        else:
            line += 1
    # Second pass
    for command in Parser.get_commands():
        if command.type == Command.A_COMMAND:
            if not str(command.content).isnumeric():
                if not symbols_table.contains(command.content):
                    # a new variable
                    symbols_table.add_variable(command.content)
                command.content = symbols_table.get_address(command.content)
        elif command.type == Command.L_COMMAND:
            continue
        hack_lines.append(Code.code(command))

    #writes the hack file
    with open(file_name[:-ASM_SUFF_LEN] + HACK_SUFF, mode=W_FILE_MODE, encoding=DEF_ENCODING) as hack_file:
        for line in hack_lines:
            hack_file.write('%s\n' % line)

def main():
    """ runs the assembler on the given argument (Assembler.py <file_name>)
    """
    file_name = sys.argv[1]

    if os.path.isfile(file_name):
        parse_asm_file(file_name)
    elif os.path.isdir(file_name):
        os.chdir(file_name)
        for f in os.listdir():
            if f.endswith(ASM_SUFF):
                parse_asm_file(f)
        os.chdir('..')

if __name__ == "__main__":
    main()
