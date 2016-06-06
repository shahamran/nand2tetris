from JackTokenizer import *
from VMWriter import *
from SymbolTable import *
import pdb

OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UN_OPS = ['-', '~']



class CompilationEngine:
    """
    Prints a valid xml file from a given Jack code.
    """
    # Variables
    tokenizer = None
    writer = None
    classname = ''
    symtable = None
    curr_subroutine = ('','', False)
    while_count = 0
    if_count = 0

    def __str__(self):
        return '\n'.join(self.writer.output)

    def __init__(self, in_file):
        # Reset data
        self.if_count, self.while_count = 0, 0
        self.curr_subroutine = ('','',False)
        self.writer = VMWriter(in_file)
        self.symtable = SymbolTable()
        self.classname = in_file.split('/')[-1][:-5]

        self.first_pass(in_file)

        # Set the tokenizer with the input file
        # pdb.set_trace() # <=========== HERE ===========
        self.tokenizer = JackTokenizer(in_file)
        # Go to the first line (token), and write the class XML
        self.tokenizer.advance()
        self.compile_class()

    def print_error(self, error_msg):
        pdb.set_trace() # <============== HERE =============
        print("In " + self.classname + " (line " + str(self.tokenizer.line_num)
              + "): " + error_msg)
        sys.exit(1)


    def assert_char(self, expected):
        actual = self.tokenizer.token.content
        line_num = self.tokenizer.line_num
        if actual != expected:
            self.print_error("Expected '" + expected + "'. Got: " + actual)
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        

    def first_pass(self, filename):
        tokens = JackTokenizer(filename)
        while tokens.has_more_tokens():
            tokens.advance()
            if tokens.token.content in ['constructor', 'method', 'function']:
                arg_count = 1 if tokens.token.content == 'method' else 0
                var_count = 0
                tokens.advance() # method...
                func_type = tokens.token.content
                tokens.advance() # type
                func_name = self.classname + '.' + tokens.token.content
                tokens.advance() # name
                # Count arguments
                tokens.advance() # (
                if tokens.token.content != ')':
                    while tokens.token.content != ')':
                        if tokens.token.content == ',':
                            arg_count += 1
                        tokens.advance()
                    arg_count += 1
                tokens.advance() # )
                tokens.advance() # {
                # Count local variables
                while tokens.token.content != '}':
                    if tokens.token.content == 'var':
                        var_count += 1
                        while tokens.token.content != ';':
                            tokens.advance()
                            if tokens.token.content == ',':
                                var_count += 1
                    tokens.advance()
                self.symtable.dec_functions[func_name] = (arg_count, var_count)


    def compile_class(self):
        """
        Writes the tokens of a class object.
        """
        # class className {
        self.assert_char('class')
        class_name = self.tokenizer.token.content
        # Ensure the class name is legal
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            self.print_error("Illegal class name: '" + class_name + "'")
        # And matches the file name
        if class_name != self.classname:
            self.print_error("The class name must match the file name.")
        self.tokenizer.advance() # className

        self.assert_char('{')
        
        while (self.tokenizer.token.content in ['field', 'static']):
            self.compile_classvar()

        while (self.tokenizer.token.content in ['constructor', 'function',
                                                'method']):
            self.compile_subroutine()

        self.assert_char('}')
        if self.tokenizer.has_more_tokens():
            self.print_error("ERROR! ERROR! ERROR! ABANDON SHIP!")


    def compile_classvar(self):
        var_kind = self.tokenizer.token.content
        if var_kind == 'field':
            var_kind = 'this'

        self.tokenizer.advance() # static|field
        vartype = self.compile_type()
        varname = self.compile_name()
        self.symtable.define(var_kind, varname, vartype)

        # Compiles: (',' name)*
        while self.tokenizer.token.content == ',':
            self.tokenizer.advance()
            varname = self.compile_name()
            self.symtable.define(var_kind, varname, vartype)

        self.assert_char(';')


    def compile_type(self):
        vartype = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            if vartype not in ['char', 'int', 'boolean']:
                self.print_error("Illegal variable type: '" + vartype + "'")
        self.tokenizer.advance() # type
        return vartype


    def compile_name(self):
        varname = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            self.print_error("Illegal variable name: '" + varname + "'")
        self.tokenizer.advance() # name
        return varname


    def compile_subroutine(self):
        routine_type = self.tokenizer.token.content
        self.tokenizer.advance()
        
        func_type = self.tokenizer.token.content
        if self.tokenizer.token.ttype != Token.IDENTIFIER:
            if func_type not in ['char', 'int', 'boolean', 'void']:
                self.print_error("Illegal function type: '" + vartype + "'")
        self.tokenizer.advance() # type
        func_name = self.classname + '.' + self.compile_name() # name

        self.curr_subroutine = func_name, func_type, routine_type == 'constructor'

        self.assert_char('(')

        # pdb.set_trace() # <=========== HERE ===================

        self.symtable.start_subroutine()
        self.writer.write_function(func_name, self.symtable.dec_functions[func_name][1])

        if routine_type == 'constructor':
            if func_type != self.classname:
                self.print_error("The return type of a constructor must be of \
                                 the class type")
            self.writer.write_push('constant', self.symtable.var_count('this'))
            self.writer.write_call('Memory.alloc', 1)
            self.writer.write_pop('pointer', 0)
        elif routine_type == 'method':
            self.writer.write_push('argument', 0)
            self.writer.write_pop('pointer', 0)

        # Compile parameter list
        self.compile_paramlist()

        self.assert_char(')')

        # Compile subroutine body
        self.compile_subroutine_body()

        self.symtable.end_subroutine()


    def compile_paramlist(self):
        while self.tokenizer.token.content != ')':
            vartype = self.compile_type()
            varname = self.compile_name()
            self.symtable.define('argument', varname, vartype)    

            if self.tokenizer.token.content != ',':
                break
            else:
                self.tokenizer.advance() # ,


    def compile_subroutine_body(self):
        self.assert_char('{')

        # Print var decleration
        while self.tokenizer.token.content == 'var':
            self.compile_vardec()

        # compile statements
        self.compile_statements()

        self.assert_char('}')


    def compile_vardec(self):
        self.tokenizer.advance() # var

        vartype = self.compile_type()
        varname = self.compile_name()
        self.symtable.define('local', varname, vartype)

        while self.tokenizer.token.content == ',':
            self.tokenizer.advance() # ,
            varname = self.compile_name()
            self.symtable.define('local', varname, vartype)

        self.assert_char(';')


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
            self.print_error('Cannot assign to an undeclared variable: ' + varname)
        vartype = self.symtable.type_of(varname)
        self.tokenizer.advance() # varName

        # Checks for array access
        if self.tokenizer.token.content == '[':
            self.compile_array_access(varname)
            is_array = True

        self.assert_char('=')
        exp_type = self.compile_expression()

        if not is_array and vartype and exp_type and vartype != exp_type:
            self.print_error(str(exp_type) + " is illegal here")
        
        if is_array:
            self.writer.write_pop('that', 0)
        else:
            self.writer.write_pop(self.symtable.kind_of(varname),
                                  self.symtable.index_of(varname))
        self.assert_char(';')


    def compile_if(self):
        # Prints if (
        self.tokenizer.advance() # if
        self.assert_char('(')

        curr_if = self.if_count
        self.if_count += 1

        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if('IF_FALSE' + str(curr_if))

        self.assert_char(')')
        self.assert_char('{')
        
        self.compile_statements()

        self.assert_char('}')

        self.writer.write_goto('IF_END' + str(curr_if))
        self.writer.write_label('IF_FALSE' + str(curr_if))

        if self.tokenizer.token.content == 'else':
            self.tokenizer.advance() # else
            self.assert_char('{')
            self.compile_statements()
            self.assert_char('}')

        self.writer.write_label('IF_END' + str(curr_if))


    def compile_while(self):
        # while (
        self.tokenizer.advance();
        self.assert_char('(')

        curr_while = self.while_count
        self.while_count += 1

        # Print while condition label
        self.writer.write_label('WHILE_EXP' + str(curr_while))
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if('WHILE_END' + str(curr_while))

        self.assert_char(')')

        self.assert_char('{')
        self.compile_statements()
        self.assert_char('}')

        self.writer.write_goto('WHILE_EXP' + str(curr_while))
        self.writer.write_label('WHILE_END' + str(curr_while))


    def compile_do(self):
        self.tokenizer.advance() # do
        self.compile_subroutine_call()
        self.assert_char(';')
        self.writer.write_pop('temp', 0)


    def compile_return(self):
        self.tokenizer.advance() # return
        curr_token = self.tokenizer.token.content
        if curr_token != ';' and self.curr_subroutine[1] != 'void':
            if self.curr_subroutine[2]:
                if curr_token != 'this':
                    self.print_error("Constructor should return 'this'")
            self.compile_expression()
        elif curr_token != ';' and self.curr_subroutine[1] == 'void':
            self.print_error('void subroutine ' + curr_subroutine[0] + ' \
                             should not return any value.')
        elif curr_token == ';' and self.curr_subroutine[1] == 'void':
            self.writer.write_push('constant', 0)
        else:
            self.print_error('Function ' + curr_subroutine[0] + ' should \
                             return a value.')

        self.writer.write_return();
        self.assert_char(';')


    def compile_expression(self):
        exp_type = self.compile_term()
        op_type = None
        while self.tokenizer.token.content in OPS:
            op = self.tokenizer.token.content
            self.tokenizer.advance() # op
            op_type = self.compile_term()
            if op_type and exp_type and op_type != exp_type:
                self.print_error(str(op_type) + " is illegal here")
            self.writer.write_arithmetic(op)


    def compile_array_access(self, varname):
        # Push var
        self.compile_push_varname(varname)
        # Push index
        self.tokenizer.advance() # [
        self.compile_expression()
        self.assert_char(']')
        # Get *(var + index)
        self.writer.write_arithmetic('add')
        # write the result into 'that'
        self.writer.write_pop('pointer', 1)


    def compile_push_varname(self, varname):
        var_kind = self.symtable.kind_of(varname)
        var_index = self.symtable.index_of(varname)
        if not var_kind:
            self.print_error('No such variable ' + varname)
        self.writer.write_push(var_kind, var_index)


    def compile_pop_varname(self, varname):
        var_kind = self.symtable.kind_of(varname)
        var_index = self.symtable.index_of(varname)
        if not var_kind:
            self.print_error('No such variable ' + varname)
        self.writer.write_pop(var_kind, var_index)


    def compile_term(self):
        # Check what kind of term
        # Constant case:
        ret_val = None
        if self.tokenizer.token.ttype in [Token.INT_CONST, Token.STR_CONST, Token.KEYWORD]:
            if self.tokenizer.token.ttype == Token.INT_CONST:
                self.writer.write_push('constant', int(self.tokenizer.token.content))
                ret_val = 'int'
            elif self.tokenizer.token.ttype == Token.STR_CONST:
                self.writer.write_string_const(self.tokenizer.token.content)
                ret_val = 'String'
            elif self.tokenizer.token.ttype == Token.KEYWORD:
                ret_val = self.writer.write_keyword_const(self.tokenizer.token.content)
                if ret_val not in ['null', 'this', 'boolean']:
                    self.print_error("Illegal keyword in term")
            self.tokenizer.advance()
            return ret_val

        # Check if unary op
        if self.tokenizer.token.content in UN_OPS:
            op = self.tokenizer.token.content
            self.tokenizer.advance() # op
            ret_val = self.compile_term()
            if op == '-':
                self.writer.write_arithmetic('neg')
            elif op == '~':
                self.writer.write_arithmetic('not')

            return ret_val
        
        # Check if bracketed expression
        if self.tokenizer.token.content == '(':
            self.tokenizer.advance()    # (
            ret_val = self.compile_expression()
            self.assert_char(')')
            return ret_val

        # Peek to next token
        prev_token = self.tokenizer.token
        self.tokenizer.advance()

        # varName[expression]
        if self.tokenizer.token.content == '[':
            # Get variable name and kind
            varname = prev_token.content
            self.compile_array_access(varname)
            self.writer.write_push('that', 0)
            return None

        # subroutineCall
        if self.tokenizer.token.content in ['(', '.']:
            self.compile_subroutine_call(prev_token)
            return None

        # Otherwise, just print last token (varName)
        self.compile_push_varname(prev_token.content)
        ret_val = self.symtable.type_of(prev_token.content)
        return ret_val if ret_val in PRIMITIVES else None


    def compile_subroutine_call(self, prev_token = None):
        caller = ''
        nargs = 0
        if not prev_token:
            caller = self.tokenizer.token.content
            self.tokenizer.advance()
        else:
            caller = prev_token.content

        if self.symtable.kind_of(caller):
            # This means the caller is a varName
            nargs += 1
            self.compile_push_varname(caller)
            caller_type = self.symtable.type_of(caller)
        else:
            # className
            caller_type = caller

        if self.tokenizer.token.content == '.':
            self.tokenizer.advance() # .
            subroutine_name = caller_type + '.' + self.tokenizer.token.content
            self.tokenizer.advance() # subroutineName
            # Now we're in (
        else:
            # This means this is an internal method call - do foo()
            nargs += 1
            self.writer.write_push('pointer', 0)
            subroutine_name = self.classname + '.' + caller


        self.assert_char('(')
        nargs += self.compile_expression_list()
        self.assert_char(')')
        
        class_name = subroutine_name.split('.')[0]
        
        if class_name == self.classname:
            if subroutine_name not in self.symtable.dec_functions:
                self.print_error("Function or method " + subroutine_name + " doesn't exist")
            elif self.symtable.dec_functions[subroutine_name][0] != nargs:
                self.print_error("Function " + subroutine_name + " gets " + \
                            str(self.symtable.dec_functions[subroutine_name][0]) + " \
                                 arguments. Got: " + str(nargs))

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

