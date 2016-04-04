class SymbolsTable:
	'A wrapper for a dictionary that holds all symbols in an asm file'
	symbols = {}
	var_num = 16

	def __init__(self):
    	""" Constructor for the symbols table object.
        Adds all predefined symbols upon creation.
        """
		for i in range(16):
			self.symbols['R' + str(i)] = i
		self.symbols['SP'] = 0
		self.symbols['LCL'] = 1
		self.symbols['ARG'] = 2
		self.symbols['THIS'] = 3
		self.symbols['THAT'] = 4
		self.symbols['SCREEN'] = 16384
		self.symbols['KBD'] = 24576
	
	def add_variable(self, var_str):
    """ Adds a variable to the symbols table and assigns an address for it, starting from 16.
        """
		self.symbols[var_str] = self.var_num
		self.var_num += 1
	
	def add_label(self, label_str, label_num):
        """ Adds a label to the symbols table with a given address
        """
		self.symbols[label_str] = label_num
	
	def contains(self, symbol):
        """ Checks whether a given symbol exists in this symbols table
        """
		return symbol in self.symbols

	def get_address(self, symbol):
        """ Returns the address of a given symbol if it exists in the table, None otherwise.
        """
		return self.symbols[symbol]
