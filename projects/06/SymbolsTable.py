class SymbolsTable:
	''
	symbols = {}
	var_num = 16

	def __init__(self):
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
		self.symbols[var_str] = self.var_num
		self.var_num += 1
	
	def add_label(self, label_str, label_num):
		self.symbols[label_str] = label_num
	
	def contains(self, symbol):
		return symbol in self.symbols

	def get_address(self, symbol):
		return self.symbols[symbol]
