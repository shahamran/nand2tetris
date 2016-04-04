import Parser,Code,Command,sys,os
from SymbolsTable import SymbolsTable
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
        if command.type == 'L':
            symbols_table.add_label(command.content, line)
        else:
            line += 1
    # Second pass
    for command in Parser.get_commands():
        if command.type == 'A':
            if not str(command.content).isnumeric():
                if not symbols_table.contains(command.content):
                    # a new variable
                    symbols_table.add_variable(command.content)
                command.content = symbols_table.get_address(command.content)
        elif command.type == 'L':
            continue
        hack_lines.append(Code.code(command))

    #writes the hack file
    with open(file_name[:-4] + '.hack', mode='w', encoding='utf-8') as hack_file:
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
            if f.endswith('.asm'):
                parse_asm_file(f)
        os.chdir('..')

if __name__ == "__main__":
    main()