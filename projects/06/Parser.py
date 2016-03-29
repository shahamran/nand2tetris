import os

class Parser:
    'Parses a given .asm file'

    # Some constants.
    COMMENT_PREFIX = '//'
    READ_ONLY = 'r'
    DEF_ENCODING = 'utf-8'
    # Data members
    file_name = ''
    lines = 0
    content = []
    # Methods
    def Parser(self, file_name):
        if file_name.endswith('.asm') and os.path.isfile(file_name):
            self.file_name = file_name
            self.parse()
        else
            print('Invalid file.')

    def parse(self):
        with open(file_name, mode=READ_ONLY, encoding=DEF_ENCODING) as asm_file:
            # Read each line
            for line in asm_file:
            # Ignore Comments...
            if line.rstrip().startswith(COMMENT_PREFIX) == False:
                content.append(line)
                lines += 1
