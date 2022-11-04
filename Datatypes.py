import logging
import collections

from CoherenceExceptions import RuleCoherenceException


class Element(object):
    def __init__(self, name : str, positive : bool):
        self.name = name
        self.positive = positive

    def __str__(self):
        sign = '' if self.positive else 'NOT '
        return f'{sign}{self.name}'
    
    def str_condensed(self)->str:
        return ('' if self.positive else 'N_')+self.name

    __repr__ = __str__

class Rule(object):
    def __init__(self, premisse : list, consequence : list):
        self.premisse = premisse
        self.consequence = consequence

    def __str__(self):
        return ((', '.join([str(elem) for elem in self.premisse])) + ' -> ' + (', '.join(str(elem) for elem in self.consequence)))

    def __hash__(self) -> int:
        str_hash = ''.join(sorted([cond.str_condensed() for cond in self.premisse]))+'_'+''.join(sorted([cond.str_condensed() for cond in self.consequence]))
        return hash(str_hash)
   
    __repr__ = __str__


class Context(object):
    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, fact : Element):
        self.facts.append(fact)
    
    def addRule(self, rule : Rule):
        self.rules.append(rule)
        try:
            self.checkRulesCoherence()
        except RuleCoherenceException as r:
                logging.error(r)
                self.rules.pop()

    def checkFactBaseCoherence(self):
        pass

    def checkRulesCoherence(self):
        self.checkRulesNoDuplicates()
    def checkRulesNoDuplicates(self):

        #Liste les hash dupliqués dans plusieurs rêgles
        duplicate_list = [item for item, count in collections.Counter( [rule.__hash__() for rule in self.rules]).items() if count > 1]

        if duplicate_list != []:
            result = []
            for dupl_hash in duplicate_list:
                dupl_rule_pack = [(f'R°{index}', rule) for index, rule in enumerate(self.rules) if rule.__hash__() == dupl_hash]
                result.append(dupl_rule_pack)

            raise RuleCoherenceException("duplicate rules found")


    def __str__(self):
        ret_str = f"{len(self.facts)} faits : \n [{', '.join([str(elem) for elem in self.facts])}] \n"
        ret_str = ret_str + f"{len(self.rules)} règles : \n " + '\n'.join([str(rule) for rule in self.rules])
        return ret_str