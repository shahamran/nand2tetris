DELIM = ' '
INDENT = '\t'

class VMWriter:
    output = []
    output_filename = ''


    def __init__(self, filename):
        if filename.endswith('.jack'):
            filename = filename[:-5]
        self.output_filename = filename + '.vm'


    def write_push(self, segment, index):
        self.output.append(INDENT + 'push' + DELIM + segment + DELIM + str(index))


    def write_pop(self, segment, index):
        self.output.append(INDENT + 'pop', + DELIM + segment + DELIM + str(index))


    def write_arithmetic(self, command):
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
        self.output.append('function' + DELIM + name + DELIM + str(nargs))


    def write_return(self):
        self.output.append(INDENT + 'return')


    def close(self):
        with open(output_filename, 'w') as f:
            f.write('\n'.join(self.output))
        return
