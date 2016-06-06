DELIM = ' '
INDENT = '\t'

class VMWriter:
    output = []
    output_filename = ''


    def __init__(self, filename):
        self.output = []
        if filename.endswith('.jack'):
            filename = filename[:-5]
        self.output_filename = filename + '.vm'


    def write_push(self, segment, index):
        self.output.append(INDENT + 'push' + DELIM + segment + DELIM + str(index))


    def write_pop(self, segment, index):
        self.output.append(INDENT + 'pop' + DELIM + segment + DELIM + str(index))


    def write_arithmetic(self, command):
        if command == '+':
            command = 'add'
        elif command == '-':
            command = 'sub'
        elif command == '*':
            self.write_call('Math.multiply', 2)
            return
        elif command == '/':
            self.write_call('Math.divide', 2)
            return
        elif command == '&':
            command = 'and'
        elif command == '|':
            command = 'or'
        elif command == '<':
            command = 'lt'
        elif command == '>':
            command = 'gt'
        elif command == '=':
            command = 'eq'

        self.output.append(INDENT + command)


    def write_label(self, label):
        self.output.append('label' + DELIM + label)


    def write_if(self, label):
        self.output.append(INDENT + 'if-goto' + DELIM + label)


    def write_goto(self, label):
        self.output.append(INDENT + 'goto' + DELIM + label)


    def write_call(self, name, nargs):
        self.output.append(INDENT + 'call' + DELIM + name + DELIM + str(nargs))


    def write_function(self, name, nlocals):
        self.output.append('function' + DELIM + name + DELIM + str(nlocals))


    def write_return(self):
        self.output.append(INDENT + 'return')


    def write_string_const(self, string):
        self.write_push('constant', len(string))
        self.write_call('String.new', 1)
        for c in string:
            self.write_push('constant', ord(c))
            self.write_call('String.appendChar', 2)
        return 'String'


    def write_keyword_const(self, keyword):
        if keyword in ['null', 'false']:
            self.write_push('constant', 0)
        elif keyword == 'true':
            self.write_push('constant', 0)
            self.write_arithmetic('not')
        elif keyword == 'this':
            self.write_push('pointer', 0)

        if keyword in ['true', 'false']:
            keyword = 'boolean'
        return keyword


    def close(self):
        with open(output_filename, 'w') as f:
            f.write('\n'.join(self.output))
        return
