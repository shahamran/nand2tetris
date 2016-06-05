from JackTokenizer import *
# import pdb

OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UN_OPS = ['-', '~']


def indent(depth):
    """
    Get the correct indentation for the given depth
    """
    return DELIM * 2 * depth


class CompilationEngine:
    """
    Prints a valid xml file from a given Jack code.
    """
    # Variables
    output = []
    tokenizer = None
    depth = 0

    def __init__(self, in_file):
        # Reset data
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


    def compile_subroutine(self):
        # Prints: keyword type name (
        self.print_tokens(4)
        # Prints parameter list
        self.print_block('parameterList', self.compile_paramlist)
        # Prints )
        self.print_tokens()
        # Prints subroutine body
        self.print_block('subroutineBody', self.compile_subroutine_body)


    def compile_paramlist(self):
        count = 2
        while self.tokenizer.token.content != ')':
            self.print_tokens(count)
            if count == 2:
                count += 1


    def compile_subroutine_body(self):
        # Print: {
        self.print_tokens()
        # Print var decleration
        while self.tokenizer.token.content == 'var':
            self.print_block('varDec', self.compile_vardec)
        # prints statements
        self.print_block('statements', self.compile_statements)
        # }
        self.print_tokens()


    def compile_vardec(self):
        # Prints var typename varname
        self.print_tokens(3)
        while self.tokenizer.token.content == ',':
            self.print_tokens(2)
        # Prints ';'
        self.print_tokens()


    def compile_statements(self):
        curr_token = self.tokenizer.token.content
        while curr_token in ['let', 'if', 'while', 'do', 'return']:
            if curr_token == 'let':
                self.print_block('letStatement', self.compile_let)
            elif curr_token == 'if':
                self.print_block('ifStatement', self.compile_if)
            elif curr_token == 'while':
                self.print_block('whileStatement', self.compile_while)
            elif curr_token == 'do':
                self.print_block('doStatement', self.compile_do)
            elif curr_token == 'return':
                self.print_block('returnStatement', self.compile_return)
            # Reload current token
            curr_token = self.tokenizer.token.content


    def compile_let(self):
        # Prints let varName
        self.print_tokens(2)
        # Checks for array access
        if self.tokenizer.token.content == '[':
            self.print_tokens() # Prints '['
            self.print_block('expression', self.compile_expression)
            self.print_tokens() # Prints ']'
        # Prints '='
        self.print_tokens()
        self.print_block('expression', self.compile_expression)
        # Prints ';'
        self.print_tokens()


    def compile_if(self):
        # Prints if (
        self.print_tokens(2)
        self.print_block('expression', self.compile_expression)
        # Print ) {
        self.print_tokens(2)
        self.print_block('statements', self.compile_statements)
        # Print }
        self.print_tokens()

        if self.tokenizer.token.content == 'else':
            self.print_tokens(2) # else {
            self.print_block('statements', self.compile_statements)
            self.print_tokens() # Print }


    def compile_while(self):
        # Print while (
        self.print_tokens(2)
        self.print_block('expression', self.compile_expression)
        # Print ) {
        self.print_tokens(2)
        self.print_block('statements', self.compile_statements)
        # Print }
        self.print_tokens()


    def compile_do(self):
        self.print_tokens() # do
        self.compile_subroutine_call()
        self.print_tokens() # ;


    def compile_return(self):
        self.print_tokens() # return
        if self.tokenizer.token.content != ';':
            self.print_block('expression', self.compile_expression)
        self.print_tokens() # ;


    def compile_expression(self):
        self.print_block('term', self.compile_term)
        while self.tokenizer.token.content in OPS:
            self.print_tokens() # op
            self.print_block('term', self.compile_term)


    def compile_term(self):
        # Check if unary op
        if self.tokenizer.token.content in UN_OPS:
            self.print_tokens()
            self.print_block('term', self.compile_term)
            return
        # Check if bracketed expression
        if self.tokenizer.token.content == '(':
            self.print_tokens() # (
            self.print_block('expression', self.compile_expression)
            self.print_tokens() # )
            return

        # Peek to next token
        prev_token = self.tokenizer.token
        self.tokenizer.advance()
        # varName[expression]
        if self.tokenizer.token.content == '[':
            self.output.append(indent(self.depth) + str(prev_token))
            self.print_tokens() # [
            self.print_block('expression', self.compile_expression)
            self.print_tokens() # ]
        # subroutineCall
        elif self.tokenizer.token.content in ['(', '.']:
            self.compile_subroutine_call(prev_token)
        # just print last token (constants / varName)
        else:
            self.output.append(indent(self.depth) + str(prev_token))


    def compile_subroutine_call(self, prev_token = None):
        if not prev_token:
            self.print_tokens()
        else:
            self.output.append(indent(self.depth) + str(prev_token))
        # (ClassName | varName).subroutineName
        if self.tokenizer.token.content == '.':
            self.print_tokens(2)

        self.print_tokens() # (
        self.print_block('expressionList', self.compile_expression_list)
        self.print_tokens() # )


    def compile_expression_list(self):
        # Check if not empty
        if self.tokenizer.token.content == ')':
            return
        # Print first expression
        self.print_block('expression', self.compile_expression)
        # and all other expressions
        while self.tokenizer.token.content == ',':
            self.print_tokens()
            self.print_block('expression', self.compile_expression)



