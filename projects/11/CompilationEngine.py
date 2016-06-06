from JackTokenizer import *
# import pdb

OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UN_OPS = ['-', '~']


def indent(depth):
    """
    Get the correct indentation for the given depth
    """
    return DELIM * 2 * depth

def print_error(error_msg):
    print(error_msg)
    exit(1)


def assert_char(expected, actual, line_num):
    if actual != expected:
        print_error("Expected '" + expected + "'. Got: " + actual + 
                    "\nLine: " + str(line_num))


class CompilationEngine:
    """
    Prints a valid xml file from a given Jack code.
    """
    # Variables
    output = []
    tokenizer = None
    depth = 0
    writer = None
    classname = ''
    symtable = None
    curr_subroutine = ('','')
    while_count = 0
    if_count = 0

    def __init__(self, in_file):
        # Reset data
        self.writer = VMWriter(in_file)
        self.symtable = SymbolTable()
        self.classname = in_file.split('/')[-1]

        self.output = []
        self.depth = 0
        # Set the tokenizer with the input file
        self.tokenizer = JackTokenizer(in_file)
        # Go to the first line (token), and write the class XML
        self.tokenizer.advance()
        self.print_block('class', self.compile_class)


    def __str__(self):
        return '\n'.join(self.output)


    def print_tokens(self, count = 1):
        """
        Print (add to output) the current token with correct indentation.
        Do this 'count' times (def = 1)
        """
        for i in range(count):
            self.output.append(indent(self.depth) + str(self.tokenizer.token))
            self.tokenizer.advance()


    def print_block(self, tag, func_name):
        """
        Prints:
            <'tag'>
                ... 'func_name's content ...
            </'tag'>
        """
        self.output.append(indent(self.depth) + open_tag(tag))
        self.depth += 1
        func_name()
        self.depth -= 1
        self.output.append(indent(self.depth) + close_tag(tag))


    def compile_class(self):
        """
        Writes the tokens of a class object.
        """
        # class className {
        self.print_tokens(3)

        while (self.tokenizer.token.content in ['field', 'static']):
            self.print_block('classVarDec', self.compile_classvar)

        while (self.tokenizer.token.content in ['constructor', 'function',
                                                'method']):
            self.print_block('subroutineDec', self.compile_subroutine)

        # }
        self.print_tokens()
        return


    def compile_classvar(self):
        # Prints: (static|field) type name
        self.print_tokens(3)
        # Prints: (',' name)*
        while (self.tokenizer.token.content == ','):
            self.print_tokens(2)
        # Prints: ';'
        self.print_tokens()


    def compile_type(self):
        vartype = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            if vartype not in ['char', 'int', 'boolean']:
                print_error("Illegal variable type: '" + vartype + "'")
        self.tokenizer.advance() # type
        return vartype


    def compile_name(self):
        varname = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            print_error("Illegal variable name: '" + varname + "'")
        self.tokenizer.advance() # name
        return varname


    def compile_subroutine(self):
        routine_type = self.tokenizer.token.content
        
        # Prints: keyword type name (
        self.print_tokens(4)
        # Prints parameter list
        self.print_block('parameterList', self.compile_paramlist)
        # Prints )
        self.print_tokens()
        # Prints subroutine body
        self.print_block('subroutineBody', self.compile_subroutine_body)


    def compile_paramlist(self):
        params_count = 0
        while self.tokenizer.token.content != ')':
            params_count += 1
            vartype = self.tokenizer.token.content
            if self.tokenizer.token.ttype != Token.IDENTIFIER:
                if vartype not in ['char', 'int', 'boolean']:
                    print_error("Illegal variable type: '" + vartype + "'")
            self.tokenizer.advance() # type

            varname = self.tokenizer.token.content
            if self.tokenizer.token.ttype != Token.IDENTIFIER:
                print_error("Illegal variable name: '" + varname + "'")
            self.symtable.define('argument', varname, vartype)    
            self.tokenizer.advance() # name

            if self.tokenizer.token.content != ',':
                assert_char(')', self.tokenizer.token.content,
                            self.tokenizer.line_num)
            else:
                self.tokenizer.advance() # ,

        self.tokenizer.advance() # )
        return params_count


    def compile_subroutine_body(self):
        assert_char('{', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # {

        # Print var decleration
        while self.tokenizer.token.content == 'var':
            self.compile_vardec()

        # compile statements
        self.compile_statements()

        assert_char('}', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # }


    def compile_vardec(self):
        self.tokenizer.advance() # var

        vartype = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            if vartype not in ['char', 'int', 'boolean']:
                print_error("Illegal variable type: '" + vartype + "'")
        self.tokenizer.advance() # type

        varname = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            print_error("Illegal variable name: '" + varname + "'")
        self.symtable.define('var', varname, vartype)    
        self.tokenizer.advance() # name
        
        while self.tokenizer.token.content == ',':
            self.tokenizer.advance() # ,
            varname = self.tokenizer.token.content
            if self.tokenizer.token.ttype != Token.IDENTIFIER:
                print_error("Illegal variable name: '" + varname + "'")
            self.symtable.define('var', varname, vartype)    
            self.tokenizer.advance() # name

        assert_char(';', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # ;


    def compile_statements(self):
        curr_token = self.tokenizer.token.content
        while curr_token in ['let', 'if', 'while', 'do', 'return']:
            if curr_token == 'let':
                self.compile_let()
            elif curr_token == 'if':
                self.compile_if()
            elif curr_token == 'while':
                self.compile_while()
            elif curr_token == 'do':
                self.compile_do()
            elif curr_token == 'return':
                self.compile_return()
            # Reload current token
            curr_token = self.tokenizer.token.content


    def compile_let(self):
        is_array = False

        # Prints let varName
        self.tokenizer.advance() # let
        varname = self.tokenizer.token.content
        if varname not in self.symtable:
            print_error('Cannot assign to an undeclared variable: ' + varname)
        vartype = self.symtable.type_of(varname)
        self.tokenizer.advance() # varName

        # Checks for array access
        if self.tokenizer.token.content == '[':
            if vartype != 'Array':
                print_error('Variable ' + varname + ' is not and array.')
            self.compile_array_access(varname)
            is_array = True

        assert_char('=', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # =
        exp_type = self.compile_expression()
        
        if is_array:
            self.writer.write_pop('that', 0)
        else:
            self.writer.write_pop(self.symtable.kind_of(varname),
                                  self.symtable.index_of(varname))
        assert_char(';', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # ;


    def compile_if(self):
        # Prints if (
        self.tokenizer.advance() # if
        assert_char('(', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # (

        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if('IF_FALSE' + str(self.if_count))

        # Print ) {
        assert_char(')', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # )
        assert_char('{', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # {
        
        self.compile_statements()

        # Print }
        assert_char('}', self.tokenizer.token.content, self.tokenizer.line_num)
        self.tokenizer.advance() # }

        self.writer.write_goto('IF_END' + str(self.if_count))
        self.writer.write_label('IF_FALSE' + str(self.if_count))

        if self.tokenizer.token.content == 'else':
            self.tokenizer.advance() # else
            assert_char('{', self.tokenizer.token.content,
                        self.tokenizer.line_num)
            self.tokenizer.advance() # {

            self.compile_statements()

            assert_char('}', self.tokenizer.token.content,
                        self.tokenizer.line_num)
            self.tokenizer.advance() # }

        self.writer.write_label('IF_END' + str(self.if_count))
        self.if_count += 1


    def compile_while(self):
        # while (
        self.tokenizer.advance();
        if self.tokenizer.token.content != '(':
            print_error("Expected '(' in the start of 'while' condition")
        self.tokenizer.advance()
        # Print while condition label
        self.writer.write_label('WHILE_EXP' + str(while_count))
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if('WHILE_END' + str(while_count))

        if self.tokenizer.token.content != ')':
            print_error("Expected ')' in the end of 'while' condition")
        self.tokenizer.advance() # )
        if self.tokenizer.token.content != '{':
            print_error("Expected '{' in the start of while statement")
        self.tokenizer.advance() # {

        self.compile_statements()

        if self.tokenizer.token.content != '}':
            print_error("Expected '}' in the end of 'while' statement")
        self.tokenizer.advance() # }

        self.writer.write_goto('WHILE_EXP' + str(while_count))
        self.writer.write_label('WHILE_END' + str(while_count))

        self.while_count += 1


    def compile_do(self):
        self.tokenizer.advance() # do
        self.compile_subroutine_call()
        if self.tokenizer.token.content != ';':
            print_error("Expected ';' after a 'do' statement")
        self.tokenizer.advance() # ;


    def compile_return(self):
        self.tokenizer.advance() # return
        if self.tokenizer.token.content != ';' and self.curr_subroutine[1] !=
        'void':
            self.compile_expression()
        elif self.tokenizer.token.content != ';' and self.curr_subroutine[1] ==
        'void':
            print_error('void subroutine ' + curr_subroutine[0] + ' should not
                        return a value.')
        elif self.tokenizer.token.content == ';' and self.curr_subroutine[1] ==
        'void':
            self.writer.write_push('constant', 0)
        else:
            print_error('Function ' + curr_subroutine[0] + ' should return a
                        value.')
        self.writer.write_return();
        if self.tokenizer.token.content != ';':
            print_error("Expected ';' after a 'return' statement")
        self.tokenizer.advance() # ;


    def compile_expression(self):
        self.compile_term()
        while self.tokenizer.token.content in OPS:
            op = self.tokenizer.token.content
            self.tokenizer.advance()
            self.compile_term()
            self.writer.write_arithmetic(op)


    def compile_array_access(self, varname):
        # Push var
        self.compile_push_varname(varname)
        # Push index
        self.tokenizer.advance() # [
        self.tokenizer.compile_expression()
        if self.tokenizer.token.content != ']':
            print_error('Expected ]. Got: ' + self.tokenizer.token.content)
        self.tokenizer.advance() # ]
        # Get *(var + index)
        self.writer.write_arithmetic('add')
        # write the result into 'that'
        self.writer.write_pop('pointer', 1)
        return


    def compile_push_varname(self, varname):
        var_kind = self.symtable.kind_of(varname)
        var_index = self.symtable.index_of(varname)
        if not var_kind:
            print_error('No such variable ' + varname)
        self.writer.write_push(var_kind, var_index)


    def compile_pop_varname(self, varname):
        var_kind = self.symtable.kind_of(varname)
        var_index = self.symtable.index_of(varname)
        if not var_kind:
            print_error('No such variable ' + varname)
        self.writer.write_pop(var_kind, var_index)


    def compile_term(self):
        # Check what kind of term
        # Constant case:
        if self.tokenizer.token.ttype in [Token.INT_CONST, Token.STR_CONST,
                                          Token.KEYWORD]:
            if self.tokenizer.token.ttype == Token.INT_CONST:
                self.writer.write_push('constant', int(self.tokenizer.token.content))
            elif self.tokenizer.token.ttype == Token.STR_CONST:
                self.writer.write_string_const(self.tokenizer.token.content)
            elif self.tokenizer.token.ttype == Token.KEYWORD:
                self.writer.write_keyword_const(self.tokenizer.token.content)
            self.tokenizer.advance()
            return

        # Check if unary op
        if self.tokenizer.token.content in UN_OPS:
            op = self.tokenizer.token.content
            self.tokenizer.advance()
            self.compile_term()
            if op == '-':
                self.writer.write_arithmetic('neg')
            elif op == '~':
                self.writer.write_arithmetic('not')
            self.tokenizer.advance()
            return
        
        # Check if bracketed expression
        if self.tokenizer.token.content == '(':
            self.tokenizer.advance()    # (
            self.compile_expression()
            if self.tokenizer.token.content != ')':
                print_error('Expected ). Got: ' + self.tokenizer.token.content)
            self.tokenizer.advance()    # )
            return

        # Peek to next token
        prev_token = self.tokenizer.token
        self.tokenizer.advance()

        # varName[expression]
        if self.tokenizer.token.content == '[':
            # Get variable name and kind
            varname = prev_token.content
            self.compile_array_access(varname)
            return

        # subroutineCall
        if self.tokenizer.token.content in ['(', '.']:
            self.compile_subroutine_call(prev_token)
            return

        # Otherwise, just print last token (varName)
        self.writer.write_varname(prev_token.content)


    def compile_subroutine_call(self, prev_token = None):
        caller = ''
        nargs = 0
        if not prev_token:
            caller = self.tokenizer.token.content
            self.tokenizer.advance()
        else:
            caller = prev_token.content

        if symtable.kind_of(caller):
            # This means the caller is a varName
            nargs += 1
            self.compile_push_varname(caller)
            caller_type = self.symtable.type_of(caller)
        else:
            # className
            caller_type = caller

        if self.tokenizer.token.content == '.':
            self.tokenizer.advance() # .
            subroutine_name = caller + '.' + self.tokenizer.token.content
            self.tokenizer.advance() # subroutineName
            # Now we're in (
        else:
            nargs += 1
            self.writer.write_push('pointer', 0)
            subroutine_name = self.classname + '.' + caller


        self.tokenizer.advance() # (
        nargs += self.compile_expression_list()
        if self.tokenizer.token.content != ')':
            print_error('Expected ). Got: ' + self.tokenizer.token.content)
        self.tokenizer.advance() # )
        
        class_name, func_name = subroutine_name.split('.')
        
        if class_name == self.classname:
            if func_name not in symtable.dec_functions:
                print_error("Function or method " + func_name + " doesn't exist")
            elif symtable.dec_functions[func_name] != nargs:
                print_error("Function " + func_name + " gets " +
                            str(symtable.dec_functions[func_name]) + " arguments.
                            Got: " + str(nargs))

        self.writer.write_call(subroutine_name, nargs)


    def compile_expression_list(self):
        expressions_count = 0
        # Check if not empty
        if self.tokenizer.token.content == ')':
            return expressions_count
        # Print first expression
        self.compile_expression()
        expressions_count += 1
        # and all other expressions
        while self.tokenizer.token.content == ',':
            self.tokenizer.advance() # ,
            self.compile_expression()
            expressions_count += 1
        return expressions_count



