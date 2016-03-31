import re
from Command import Command

def code(command):
    if command.type == 'C':
        match = re.match('(?:(^[AMD]{1,3})=)?(?:([^;]+))(?:;(J\w{2}))?', command.content)
        dest = match.group(1)
        comp = match.group(2)
        jmp  = match.group(3)
        if not jmp:
            jmp = ''
        if not dest:
            dest = ''
        dest = dest.strip(); jmp = jmp.strip(); comp = comp.strip()
        dest = parse_dest(dest)
        comp = parse_comp(comp)
        jmp  = parse_jmp(jmp)
        return '1' + comp + dest + jmp
    elif command.type == 'A':
        address = dec_to_binary(int(command.content))
        return '0' * (16 - len(address)) + address

def parse_dest(dest_str):
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
    result = 0
    if 'G' in jmp_str:
        result = result | 1
    if 'L' in jmp_str:
        result = result | 4
    if 'E' in jmp_str and 'N' not in jmp_str:
        result = result | 2
    elif 'NE' in jmp_str:
        result = 5
    if jmp_str == 'JMP':
        result = 7
    result = dec_to_binary(result)
    return '0' * (3-len(result)) + result

def dec_to_binary(dec):
    return str(bin(dec)[2:])
