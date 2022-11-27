from __future__ import annotations #permet de retourner ConcreteRule dans une Rule
from abc import ABC, abstractclassmethod


class Element(object):
    def __init__(self, name : str, positive : bool):
        self.name = name
        self.positive = positive

    def __str__(self):
        sign = '' if self.positive == True else 'NOT '
        return f'{sign}{self.name}'
    
    def str_condensed(self)->str:
        return ('' if self.positive else 'N-')+self.name
    
    def __eq__(self, other):
        return other.name == self.name and other.positive == self.positive
    def __hash__(self):
        return hash(self.str_condensed())

    __repr__ = __str__

class Rule(ABC):

    def __init__(self, name : str):
        self.name = name

    @abstractclassmethod
    def satisfy(self, facts : list[Element]) -> tuple[ConcreteRule, str] | None: 
        pass

    @abstractclassmethod
    def __hash__(self) -> int:
        pass
    
    @abstractclassmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class ConcreteRule(Rule):
    def __init__(self, premisse : list[Element], consequence : list[Element], name : str):
        Rule.__init__(self, name)
        self.premisse = premisse
        self.consequence = consequence

    def satisfy(self, facts : list[Element]) -> tuple[ConcreteRule, str] | None: 
        if set(self.premisse).issubset(set(facts)):
            return (self, self.name)
        return None

    def __str__(self):
        return (self.name + ' : '+(', '.join([str(elem) for elem in self.premisse])) + ' -> ' + (', '.join(str(elem) for elem in self.consequence)))

    def __hash__(self) -> int:
        str_hash = '.'.join(sorted([cond.str_condensed() for cond in self.premisse]))+'_'+''.join(sorted([cond.str_condensed() for cond in self.consequence]))
        return hash(str_hash)
    


    __repr__ = __str__


class Metarule(Rule):
    def __init__(self, name : str, rule_list : list[ConcreteRule], sorted : bool= True):
        Rule.__init__(self, name)
        self.rule_list : list[ConcreteRule] = rule_list

        if not sorted :
            self.rule_list.sort(key=lambda rule : rule.name)

    def satisfy(self, facts : list[Element]) -> tuple[ConcreteRule, str] | None: 
        for rule in self.rule_list:
            ret = rule.satisfy(facts)
            if ret : 
                return (rule, self.name)    
        return None

    def __str__(self):
        return (f'[{self.name}  : '+(' > '.join([str(rule.name) for rule in self.rule_list]))+"]" )

    def __hash__(self) -> int:
        final_hash : int = 0
        for hs in self.rule_list:
            final_hash += hs.__hash__()
        return hash(final_hash)