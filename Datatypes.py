class Element(object):
    def __init__(self, name : str, positive : bool):
        self.name = name
        self.positive = positive

    def __str__(self):
        sign = '' if self.positive else 'NOT '
        return f'{sign}{self.name}'
    
    def str_condensed(self)->str:
        return ('' if self.positive else 'N-')+self.name
    
    def __eq__(self, other):
        return other.name == self.name and other.positive == self.positive

    __repr__ = __str__

class Rule(object):
    def __init__(self, premisse : list, consequence : list):
        self.premisse = premisse
        self.consequence = consequence

    def __str__(self):
        return ((', '.join([str(elem) for elem in self.premisse])) + ' -> ' + (', '.join(str(elem) for elem in self.consequence)))

    def __hash__(self) -> int:
        str_hash = '.'.join(sorted([cond.str_condensed() for cond in self.premisse]))+'_'+''.join(sorted([cond.str_condensed() for cond in self.consequence]))
        return hash(str_hash)
   
    __repr__ = __str__
