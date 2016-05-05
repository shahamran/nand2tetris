import Parser,CodeWriter,sys,os
from Command import Command

# Constants:
VM_SUFF = ".vm"
ASM_SUFF = ".asm"
W_FILE_MODE = "w"
DEF_ENCODING = "utf-8"

""" The vmtranslator main file.
"""
def parse_vm_file(file_name):
    """ Gets the commands list using the parser and scans it twice
        first time searching for labels, second time uses the code to translate
        the A and C commands to machine code.
        Adds the machine code to a new .asm file
        Input: file_name - the .vm file needed to be translated
        Output: the translated file_name.asm file
    """
    Parser.parse(file_name)
    CodeWriter.set_vm_file(file_name)
    for command in Parser.get_commands():
        if command.type == Parser.CommandType.C_ARITHMETIC:
            CodeWriter.write_arithmetic(command.content[0])
        elif command.type == Parser.CommandType.C_PUSH or \
              command.type == Parser.CommandType.C_POP:
            CodeWriter.write_push_pop(command.type, command.content[1], command.content[2])
            
def main():
    """ runs the assembler on the given argument (Assembler.py <file_name>)
    """
    file_name = sys.argv[1]

    if os.path.isfile(file_name):
        CodeWriter.set_asm_file(file_name[:-len(VM_SUFF)] + ASM_SUFF)
        parse_vm_file(file_name)
    elif os.path.isdir(file_name):
        if file_name.endswith('/'):
            file_name = file_name[:-1]
        CodeWriter.set_asm_file(os.path.abspath(file_name) + ASM_SUFF)
        os.chdir(file_name)
        for f in os.listdir():
            if f.endswith(VM_SUFF):
                parse_vm_file(f)
        os.chdir('..')
    CodeWriter.write_asm()

if __name__ == "__main__":
    main()
