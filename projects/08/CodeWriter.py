from Command import Command
import Parser


# Constants
DEF_ENCODING = "utf-8"
INIT_STR = '@END\n0;JMP\n(WRITE_EQ)\n@R15\nM=D\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_EQ\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_EQ)\n@R15\nA=M\n' +\
    '0;JMP\n(WRITE_GT)\n@R15\nM=D\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_GT\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_GT)\n' + \
    '@R15\nA=M\n0;JMP\n(WRITE_LT)\n@R15\nM=D\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_LT\nD;JGE\n@SP\nA=M-1\nM=-1\n' + \
    '(END_LT)\n@R15\nA=M\n0;JMP\n(END)\n@END\n0;JMP\n'

VM_SUFF = ".vm"

SEG_CONSTANT = 'constant'
SEG_ARGUMENT = 'argument'
SEG_LOCAL = 'local'
SEG_STATIC = 'static'
SEG_THIS = 'this'
SEG_THAT = 'that'
SEG_POINTER = 'pointer'
SEG_TEMP = 'temp'

# Variables
line_num = 0
jmp_counter = 0
static_counter = 0
vm_file = ''
asm_file_name = ''
content = []


def set_asm_file(filename):
    global asm_file_name
    global content
    asm_file_name = filename
    content = []
    with open(asm_file_name, mode='w', encoding=DEF_ENCODING) as asm_file:
        i=0


def write_asm():
    with open(asm_file_name, mode='a', encoding=DEF_ENCODING) as asm_file:
        for command in content:
            asm_file.write('%s\n' % command)
        asm_file.write(INIT_STR)


def set_vm_file(filename):
    global content
    global static_counter
    global vm_file
    with open(asm_file_name, mode='a', encoding=DEF_ENCODING) as asm_file:
        for command in content:
            asm_file.write('%s\n' % command)
    static_counter = 0
    content = []
    vm_file = filename.split('/')[-1]


def write_unary_op():
    content.append('@SP')
    content.append('A=M-1')


def write_binary_op():
    content.append('@SP')
    content.append('AM=M-1')
    content.append('D=M')
    content.append('A=A-1')


def write_arithmetic(command):
    global jmp_counter
    global content
    if command == Command.A_ADD:
        write_binary_op()
        content.append('M=D+M')
    elif command == Command.A_SUB:
        write_binary_op()
        content.append('M=M-D')
    elif command == Command.A_EQ:
        content.append('@RET_ADDRESS' + str(jmp_counter))
        content.append('D=A')
        content.append('@WRITE_EQ')
        content.append('0;JMP')
        content.append('(RET_ADDRESS' + str(jmp_counter) + ')')
        jmp_counter += 1
    elif command == Command.A_LT:
        content.append('@RET_ADDRESS' + str(jmp_counter))
        content.append('D=A')
        content.append('@WRITE_LT')
        content.append('0;JMP')
        content.append('(RET_ADDRESS' + str(jmp_counter) + ')')
        jmp_counter += 1
    elif command == Command.A_GT:
        content.append('@RET_ADDRESS' + str(jmp_counter))
        content.append('D=A')
        content.append('@WRITE_GT')
        content.append('0;JMP')
        content.append('(RET_ADDRESS' + str(jmp_counter) + ')')
        jmp_counter += 1
    elif command == Command.A_NEG:
        write_unary_op()
        content.append('M=-M')
    elif command == Command.A_AND:
        write_binary_op()
        content.append('M=D&M')
    elif command == Command.A_OR:
        write_binary_op()
        content.append('M=D|M')
    elif command == Command.A_NOT:
        write_unary_op()
        content.append('M=!M')

def write_push_pop(push_pop, segment, index):
    index = int(index)
    global content
    static_name = vm_file[:-len(VM_SUFF)]
    if push_pop == Parser.CommandType.C_PUSH:
        if segment == SEG_CONSTANT:
            content.append('@' + str(index))
            content.append('D=A')
        elif segment == SEG_LOCAL:
            content.append('@LCL')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('A=D+A')
            content.append('D=M')
        elif segment == SEG_ARGUMENT:
            content.append('@ARG')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('A=D+A')
            content.append('D=M')
        elif segment == SEG_THIS:
            content.append('@THIS')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('A=D+A')
            content.append('D=M')
        elif segment == SEG_THAT:
            content.append('@THAT')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('A=D+A')
            content.append('D=M')
        elif segment == SEG_POINTER:
            content.append('@R' + str(3 + index))
            content.append('D=M')
        elif segment == SEG_TEMP:
            content.append('@R' + str(5 + index))
            content.append('D=M')
        elif segment == SEG_STATIC:
            content.append('@' + static_name + '.' + str(index))
            content.append('D=M')
        content.append('@SP')
        content.append('A=M')
        content.append('M=D')
        content.append('@SP')
        content.append('M=M+1')

    elif push_pop == Parser.CommandType.C_POP:
        if segment == SEG_LOCAL:
            content.append('@LCL')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('D=D+A')
        elif segment == SEG_ARGUMENT:
            content.append('@ARG')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('D=D+A')
        elif segment == SEG_THIS:
            content.append('@THIS')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('D=D+A')
        elif segment == SEG_THAT:
            content.append('@THAT')
            content.append('D=M')
            content.append('@' + str(index))
            content.append('D=D+A')
        elif segment == SEG_POINTER:
            content.append('@R' + str(3 + index))
            content.append('D=A')
        elif segment == SEG_TEMP:
            content.append('@R' + str(5 + index))
            content.append('D=A')
        elif segment == SEG_STATIC:
            content.append('@' + static_name + '.' + str(index))
            content.append('D=A')
        content.append('@R13')
        content.append('M=D')
        content.append('@SP')
        content.append('AM=M-1')
        content.append('D=M')
        content.append('@R13')
        content.append('A=M')
        content.append('M=D')

def writeLabel(label):
    global content
    content.append('(' + label + ')')

def writeGoto(label):
    global content
    content.append('@' + label)
    content.append('0;JMP')

def writeIf(label):
    global content
    content.append('@SP')
    content.append('AM=M-1')
    content.append('D=M')
    content.append('@' + label)
    content.append('D;JNE')

def writePush():
    """ Increases the stack size by 1 and changes the current address
    to the previous SP location
    """
    global content
    content.append('@SP')
    content.append('M=M+1')
    content.append('A=M-1')

def writePushSeg(seg):
    global content
    content.append('@' + seg)
    content.append('D=M')
    writePush()
    content.append('M=D')

def writeCall(funcName, numArgs):
    global jmp_counter
    global content
    # push return address
    content.append('@RET_ADDRESS' + str(jmp_counter))
    content.append('D=A')
    writePush()
    content.append('M=D')
    # push LCL
    writePushSeg('LCL')
    # push ARG
    writePushSeg('ARG')
    # push THIS
    writePushSeg('THIS')
    # push THAT
    writePushSeg('THAT')
    # ARG = SP-n-5
    content.append('@' + str(numArgs))
    content.append('D=A')
    content.append('@5')
    content.append('D=D+A')
    content.append('@SP')
    content.append('D=M-D')
    content.append('@ARG')
    content.append('M=D')
    # LCL = SP
    content.append('@SP')
    content.append('D=M')
    content.append('@LCL')
    content.append('M=D')
    # transfer control
    writeGoto(funcName)
    # return address
    writeLabel('RET_ADDRESS' + str(jmp_counter))

    jmp_counter += 1

def writeSegFrame(seg, frame, num):
    global content
    content.append('@' + frame)
    content.append('D=M')
    content.append('@' + str(num))
    content.append('A=D-A')
    content.append('D=M')
    content.append('@' + seg)
    content.append('M=D')

def writeReturn():
    global content
    FRAME = 'R14'
    RET = 'R13'
    # FRAME = LCL
    content.append('@LCL')
    content.append('D=M')
    content.append('@' + FRAME)
    content.append('M=D')
    # RET=*(FRAME-5)
    writeSegFrame(RET, FRAME, 5)
    # *ARG=pop()
    content.append('@SP')
    content.append('AM=M-1')
    content.append('D=M')
    content.append('@ARG')
    content.append('A=M')
    content.append('M=D')
    # SP=ARG+1
    content.append('@ARG')
    content.append('D=M+1')
    content.append('@SP')
    content.append('M=D')
    # THAT=*(FRAME-1)
    writeSegFrame('THAT', FRAME, 1)
    # THIS=*(FRAME-2)
    writeSegFrame('THIS', FRAME, 2)
    # ARG=*(FRAME-3)
    writeSegFrame('ARG', FRAME, 3)
    # LCL=*(FRAME-4)
    writeSegFrame('LCL', FRAME, 4)
    # goto RET
    content.append('@' + RET)
    content.append('A=M')
    content.append('0;JMP')
        

def writeFunction(funcName, numLocals):
    global content
    writeLabel(funcName)
    for i in range(int(numLocals)):
            writePush()
            content.append('M=0')

def writeInit():
    global content
    content = ['@256', 'D=A', '@SP', 'M=D']
    writeCall('Sys.init', 0)


