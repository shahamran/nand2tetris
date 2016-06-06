PRIMITIVES = ['int', 'char', 'boolean']

class Scope:
    # static variable
    static_count = 0
    # nonstatic
    field_count, arg_count, var_count = 0, 0, 0
    dic = {} # Values: (KIND, type, index)

    def __init__(self):
        self.dic = {}
        self.field_count, self.arg_count, self.var_count = 0, 0, 0


    def add_val(self, kind, name, stype):
        index = 0
        if kind == 'static':
            index = self.static_count
            Scope.static_count += 1
        elif kind == 'this':
            index = self.field_count
            self.field_count += 1
        elif kind == 'argument':
            index = self.arg_count
            self.arg_count +=1
        elif kind == 'local':
            index = self.var_count
            self.var_count += 1

        self.dic[name] = (kind, stype, index)


class SymbolTable:
    dec_functions = {}
    scopes = []


    def __init__(self):
        self.dec_functions = {}
        self.scopes = []
        self.start_subroutine()


    def start_subroutine(self):
        self.scopes.append(Scope())


    def end_subroutine(self):
        self.scopes = self.scopes[:-1]


    def define(self, kind, name, stype):
        if stype == 'char':
            stype = 'int'
        if len(self.scopes) == 0:
            return

        self.scopes[-1].add_val(kind, name, stype)


    def var_count(self, kind):
        if len(self.scopes) == 0:
            return 0

        if kind == 'static': # STATIC
            return Scope.static_count
        
        if kind == 'this': # FIELD
            return self.scopes[0].field_count
        elif kind == 'argument': # ARG
            return self.scopes[-1].arg_count
        elif kind == 'local': # VAR
            return self.scopes[-1].var_count
        return


    def kind_of(self, name):
        for i in reversed(range(len(self.scopes))):
            if name in self.scopes[i].dic.keys():
                return self.scopes[i].dic[name][0]
        return None


    def type_of(self, name):
        for i in reversed(range(len(self.scopes))):
            if name in self.scopes[i].dic.keys():
                type_name = self.scopes[i].dic[name][1]
                return type_name
        return None


    def index_of(self, name):
        for i in reversed(range(len(self.scopes))):
            if name in self.scopes[i].dic.keys():
                return self.scopes[i].dic[name][2]
        return None


    def __contains__(self, varname):
        for i in range(len(self.scopes)):
            if varname in self.scopes[i].dic:
                return True
        return False
