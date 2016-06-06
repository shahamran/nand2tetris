
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
        if kind == 'STATIC':
            index = self.static_count
            Scope.static_count += 1
        elif kind == 'FIELD':
            index = self.field_count
            self.field_count += 1
        elif kind == 'ARG':
            index = self.arg_count
            self.arg_count +=1
        elif kind == 'VAR':
            index = self.var_count
            self.var_count += 1

        self.dic[name] = (kind, stype, index)


class SymbolTable:
    scopes = []


    def __init__(self):
        self.start_subroutine()


    def start_subroutine(self):
        self.scopes.append(Scope())


    def define(self, kind, name, stype):
        if len(self.scopes) == 0:
            return

        self.scopes[-1].add_val(kind, name, stype)


    def var_count(self, kind):
        if len(self.scopes) == 0:
            return 0

        if kind == 'static': # STATIC
            return Scope.static_count
        
        if kind == 'this': # FIELD
            return self.scopes[-1].field_count
        elif kind == 'argument': # ARG
            return self.scopes[-1].arg_count
        elif kind == 'local': # VAR
            return self.scopes[-1].var_count
        return


    def kind_of(self, name):
        if name in self.scopes[-1].dic.keys():
            return self.scopes[-1].dic[name][0]
        else:
            return None


    def type_of(self, name):
        if name in self.scopes[-1].dic.keys():
            return self.scopes[-1].dic[name][1]
        else:
            return None


    def index_of(self, name):
        if name in self.scopes[-1].dic.keys():
            return self.scopes[-1].dic[name][2]
        else:
            return None

    def __contains__(self, varname):
        return varname in self.dic
