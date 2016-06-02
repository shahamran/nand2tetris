# Imports
import re
from enum import Enum

DELIM = ' '


def open_tag(string):
    return '<' + string + '>'


def close_tag(string):
    return '</' + string + '>'


# Token object
class Token:
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    IDENTIFIER = 'identifier'
    INT_CONST = 'integerConstant'
    STR_CONST = 'stringConstant'

    ttype = ''
    content = ''

    def __init__(self, ttype, content):
        self.ttype = ttype
        self.content = content


    def __str__(self):
        temp = self.content.replace('&', '&amp')
        temp = temp.replace('<', '&lt')
        temp = temp.replace('>', '&gt')
        return open_tag(self.ttype) + DELIM + temp + DELIM + close_tag(self.ttype)
    

    def __repr__(self):
        return str(self)

# End Token Class

class JackTokenizer:
    # Constants
    KEYWORDS_STR = ['class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                'this', 'let', 'do', 'if', 'else', 'while', 'return']
    SYMBOLS_STR = ['{', '}', '\(', '\)', '\[', '\]', '\.', ',', ';', '\+', '-', '\*', '/',
                   '&', '\|', '<', '>', '=', '~']

    # Regexes
    KEYWORDS_RGX = re.compile('\s*(' + '|'.join(KEYWORDS_STR) + ')\s*')
    SYMBOLS_RGX = re.compile('\s*(' + '|'.join(SYMBOLS_STR) + ')\s*')
    INT_RGX = re.compile('\s*(\d+)\s*')
    STR_RGX = re.compile('\s*"([^"]*)"s*')
    IDENTIFIER_RGX = re.compile('\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*')
    COMMENT_RGX = re.compile('\s*//.*$|/\*(?:.|[\n])*?\*/\s*', re.M)
    LINE_END_RGX = re.compile('\s*;\s*', re.M)

    # Variables
    content = ''
    token = None


    def __init__(self, fileName):

        with open(fileName,'r') as f:
            self.content = f.read()


    def has_more_tokens(self):
        return len(self.content.strip()) > 0


    def token_type(self):
        return self.token.ttype


    def token_content(self):
        return self.token.content


    def advance(self):
        if not self.has_more_tokens():
            return
        
        is_comment = False
        match_obj = None
        token_type = None
        
        if self.COMMENT_RGX.match(self.content):
            match_obj = self.COMMENT_RGX.match(self.content)
            is_comment = True

        elif self.KEYWORDS_RGX.match(self.content):
            match_obj = self.KEYWORDS_RGX.match(self.content)
            token_type = Token.KEYWORD

        elif self.SYMBOLS_RGX.match(self.content):
            match_obj = self.SYMBOLS_RGX.match(self.content)
            token_type = Token.SYMBOL

        elif self.INT_RGX.match(self.content):
            match_obj = self.INT_RGX.match(self.content)
            token_type = Token.INT_CONST

        elif self.STR_RGX.match(self.content):
            match_obj = self.STR_RGX.match(self.content)
            token_type = Token.STR_CONST

        elif self.IDENTIFIER_RGX.match(self.content):
            match_obj = self.IDENTIFIER_RGX.match(self.content)
            token_type = Token.IDENTIFIER
        
        if not match_obj:
            return

        self.content = self.content[match_obj.end():]

        if is_comment:
            self.advance()
        else:
            self.token = Token(token_type, match_obj.group(1))
    
