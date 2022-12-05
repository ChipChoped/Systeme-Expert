from __future__ import annotations #permet de retourner ConcreteRule dans une Rule
from abc import ABC, abstractclassmethod
from enum import Enum
from CoherenceExceptions import ConstraintCoherenceException

class VariableTypes(Enum):
    BOOLEAN = 1
    NUMBER = 2
    ENUM = 3
    
    def __int__(self):
        return self.value


class OperatorTypes(Enum):
    EQUALS = 0
    GREATER = 1
    GREATER_OR_EQUAL = 2
    LESS = 3
    LESS_OR_EQUAL = 4
    
    def __int__(self):
        return self.value

op_list = ['equal', 'greater', 'greaterOrEqual', 'less', 'lessOrEqual']
    
    


class Element(ABC):
    def __init__(self, name : str, value : object, type : VariableTypes):
        self.name = name
        self.type = type
        self.value = value
    
    @abstractclassmethod
    def __str__(self) -> str:
        pass

    def override(self, value) -> bool:
        '''Essaie d'ajouter une valeur / de modifier l'actuelle
        Renvoi True si possible'''
        return False

    @abstractclassmethod
    def str_condensed(self)->str:
        pass

    def conflict(self, elem : Element) -> bool:
        return elem.name == self.name and (elem.type != self.type or elem.value != self.value)
    
    def conflicts(self, elems: list[Element]):
        return any([self.conflict(elem) for elem in elems])

    def __eq__(self, other):
        return other.name == self.name and other.value == self.value

    def __hash__(self):
        return hash(self.str_condensed())
    
    def equal(self, other)->bool:
        return other.type == self.type and other.value == self.value

    __repr__ = __str__


class Boolean(Element):
    def __init__(self, name : str, value : bool):
        super().__init__(name, value, VariableTypes.BOOLEAN)
    
    def __str__(self):
        sign = '' if self.value else 'NOT '
        return f'{sign}{self.name}'
    
    def str_condensed(self)->str:
        return ('' if self.value else 'N-')+self.name
    
    __repr__ = __str__


class Number(Element):
    def __init__(self, name : str, value : int | float):
        super().__init__(name, value, VariableTypes.NUMBER)
    
    def __str__(self):
        return f'{self.name}[{self.value}]'
    
    def str_condensed(self)->str:
        return f'{self.name}[{self.value}]'

    def greater(self, other) -> bool:
        return other.type == self.type and self.value > other.value

    def greaterOrEqual(self, other) -> bool:
        return other.type == self.type and self.value >= other.value

    def less(self, other) -> bool:
        return other.type == self.type and self.value < other.value
    
    def lessOrEqual(self, other) -> bool:
        return other.type == self.type and self.value <= other.value

    __repr__ = __str__
 
class EnumElem(Element):
    def __init__(self, name : str, value : dict[Boolean]):
        
        super().__init__(name, value, VariableTypes.ENUM)
    
    def __str__(self):
        return f'{self.name}[{self.value}]'
    
    def str_condensed(self)->str:
        return f'{self.name}[{self.value}]'
    
    def conflict(self, value : Element) -> bool:
        if value.type == VariableTypes.ENUM:
            return self.name == value.name and any([self.conflict(elem) for elem in list(value.value.values())])
        elif value.type == VariableTypes.BOOLEAN:
            return self.value.get(value.name) is not None and self.value.get(value.name).conflict(value)
        else:
            return False
    
    def override(self, value : Element) -> bool:
        if self.conflict(value):
            return False
        elif value.type == VariableTypes.BOOLEAN:
            self.value[value.name] = value
            return True
        elif value.type == VariableTypes.ENUM:
            self.value.update(value.value)
            return True
        else:
            return False
    
    def equal(self, element : EnumElem) -> bool:
        """l'autre enum est un subset de celle-ci"""
        return element.type == self.type and all([self.value.get(elem.name) is not None and self.value.get(elem.name) == elem for elem in list(element.value.values())])

    
    __repr__ = __str__

class Constraint(object):
    def __init__(self, elem : Element, operator : OperatorTypes, positive : bool = True):
        if not callable(getattr(elem, op_list[int(operator)], None)):
            raise ConstraintCoherenceException(f"The {elem.type} {elem.name} can't use the operator {op_list[int(operator)]}")
        self.elem = elem
        self.operator = operator 
        self.positive = positive

    def str_condensed(self):
        return self.elem.name +"_"+op_list[int(self.operator)]+"_"+str(self.elem.value)
    
    def __str__(self)->str:
        return "<Contr "+self.elem.name +" "+op_list[int(self.operator)]+" "+str(self.elem.value)+">"
    
    def satisfy(self, other : Element) -> bool:
        result : bool = other.type == self.elem.type and getattr(other, op_list[int(self.operator)])(self.elem)
        return result if self.positive else not result
    
    def satisfiable(self, other : dict[Element]):
        return False if other.get(self.elem.name) is None else self.satisfy(other[self.elem.name])
    __repr__ = __str__


class Rule(ABC):

    def __init__(self, name : str):
        self.name = name

    @abstractclassmethod
    def satisfy(self, facts : list[Element]) -> tuple[ConcreteRule, str] | None: 
        pass

    @abstractclassmethod
    def concludes(self, fact: Element) -> tuple[ConcreteRule, str] | None:
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
    def __init__(self, premisse : list[Constraint], consequence : list[Element], name : str):
        super().__init__(name)
        self.premisse = premisse
        self.consequence = consequence

    def satisfy(self, facts : dict[Element]) -> tuple[ConcreteRule, str] | None: 
        if all([constraint.satisfiable(facts) for constraint in self.premisse]):
            return (self, self.name)
        return None

    def concludes(self, fact : Element) -> tuple[ConcreteRule, str] | None:
        if self.consequence.count(fact):
        # if set(self.consequence).issubset(set(facts)):
            return self, self.name
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

    def concludes(self, fact : Element) -> tuple[ConcreteRule, str] | None:
        for rule in self.rule_list:
            ret = rule.concludes(fact)
            if ret:
                return rule, self.name
        return None

    def __str__(self):
        return (f'<MetaR {self.name}  : '+(' > '.join([str(rule.name) for rule in self.rule_list]))+">" )

    def __hash__(self) -> int:
        final_hash : int = 0
        for hs in self.rule_list:
            final_hash += hs.__hash__()
        return hash(final_hash)

    __repr__ = __str__
