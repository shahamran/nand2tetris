import re
from Command import Command
"""The translates the assembler commands to machine code commands
"""
# the regex that parses a c-command to its components
C_REGEX = '(?:(^[AMD]{1,3})=)?(?:([^;]+))(?:;(J\w{2}))?'

def code(command):
    """gets an assembler command and translates and returns it as machine code
       Input: command - the command to be translates
    """
    if command.type == Command.C_COMMAND:
        # matches the C command to the dest comp and jmp parts by groups
        match = re.match(C_REGEX, command.content)
        dest = match.group(1)
        comp = match.group(2)
        jmp  = match.group(3)
        # Convert None to empty string
        if not jmp:
            jmp = ''

        if not dest:
            dest = ''

        dest = dest.strip(); jmp = jmp.strip(); comp = comp.strip()
        dest = parse_dest(dest)
        comp = parse_comp(comp)
        jmp  = parse_jmp(jmp)
        return '1' + comp + dest + jmp
    elif command.type == Command.A_COMMAND:
        address = dec_to_binary(int(command.content))
        return '0' * (16 - len(address)) + address

def parse_dest(dest_str):
    """parses the dest part of the C command to machine code
       Input: dest_str - the dest in assembler
       Output: A string representing dest in machine code
    """
    result = 0
    if 'A' in dest_str:
        result = result | 4

    if 'D' in dest_str:
        result = result | 2

    if 'M' in dest_str:
        result = result | 1

    result = dec_to_binary(result)
    return '0' * (3-len(result)) + result

def parse_comp(comp_str):
    """parses the comp part of the C command to machine code
       Input: comp_str - the comp part in assembler
       Output: A string representing dest in machine code
    """
    comp_str = comp_str.strip()
    if comp_str == '0':
        return '110' + ('10' * 3)
    elif comp_str == '1':
        return '110' + ('1' * 6)
    elif comp_str == '-1':
        return '110111010'
    elif comp_str == 'D':
        return '110001100'
    elif comp_str == 'A':
        return '110110000'
    elif comp_str == '!D':
        return '110001101'
    elif comp_str == '!A':
        return '110110001'
    elif comp_str == '-D':
        return '110001111'
    elif comp_str == '-A':
        return '110110011'
    elif comp_str == 'D+1':
        return '110011111'
    elif comp_str == 'A+1':
        return '110110111'
    elif comp_str == 'D-1':
        return '110001110'
    elif comp_str == 'A-1':
        return '110110010'
    elif comp_str == 'D+A':
        return '110000010'
    elif comp_str == 'D-A':
        return '110010011'
    elif comp_str == 'A-D':
        return '110000111'
    elif comp_str == 'D&A':
        return '110000000'
    elif comp_str == 'D|A':
        return '110010101'
    elif comp_str == 'M':
        return '111110000'
    elif comp_str == '!M':
        return '111110001'
    elif comp_str == '-M':
        return '111110011'
    elif comp_str == 'M+1':
        return '111110111'
    elif comp_str == 'M-1':
        return '111110010'
    elif comp_str == 'D+M':
        return '111000010'
    elif comp_str == 'D-M':
        return '111010011'
    elif comp_str == 'M-D':
        return '111000111'
    elif comp_str == 'D&M':
        return '111000000'
    elif comp_str == 'D|M':
        return '111010101'
    elif comp_str == 'D*A':
        return '100000000'
    elif comp_str == 'D*M':
        return '101000000'
    elif comp_str == 'D<<':
        return '010110000'
    elif comp_str == 'A<<':
        return '010100000'
    elif comp_str == 'M<<':
        return '011100000'
    elif comp_str == 'D>>':
        return '010010000'
    elif comp_str == 'A>>':
        return '010000000'
    elif comp_str == 'M>>':
        return '011000000'


def parse_jmp(jmp_str):
    """parses the jmp part of the C command to machine code
       Input: jmp_str - the jmp in assembler
       Ouetput: A string representing jmp in machine code
     """
    result = 0
    # JGE or JGT
    if 'G' in jmp_str:
        result = result | 1

    # JLE or JLT
    if 'L' in jmp_str:
        result = result | 4

    # JLE ot JGE
    if 'E' in jmp_str and 'N' not in jmp_str:
        result = result | 2

    # JNE
    elif 'NE' in jmp_str:
        result = 5

    # unconditional jump
    if jmp_str == 'JMP':
        result = 7

    result = dec_to_binary(result)
    return '0' * (3-len(result)) + result

def dec_to_binary(dec):
    """recieves a number in decimal representation and changes it to it binary representation
    """
    return str(bin(dec)[2:])
