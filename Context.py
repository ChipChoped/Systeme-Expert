from Datatypes import Element, Rule
from CoherenceExceptions import RuleCoherenceException, FactCoherenceException
import logging
import collections


class Context(object):

    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, fact : Element):
        if Element(fact.name, not fact.positive) in self.facts:
            raise FactCoherenceException(f'{fact.name} is True and False at the same time !')
        if fact not in self.facts:
            self.facts.append(fact)

    def addRule(self, rule: Rule):
        if rule in self.rules:
            raise RuleCoherenceException("duplicate rules found")
        self.rules.append(rule)
    
    def checkFactBaseCoherence(self):
        for fact in self.facts:
            if Element(fact.name, not fact.positive) in self.facts:
                raise FactCoherenceException(f'{fact.name} is True and False at the same time !')

    def checkRulesCoherence(self):
        self.checkRulesNoDuplicates()

    def checkRulesNoDuplicates(self):
        """ Deprecated, il faudrait check si une rêgle est dupliquée lors de l'insertion """
        # Liste les hash dupliqués dans plusieurs rêgles
        duplicate_list = [item for item, count in collections.Counter(
            [rule.__hash__() for rule in self.rules]).items() if count > 1]

        if duplicate_list != []:
            result = []
            for dupl_hash in duplicate_list:
                dupl_rule_pack = [(f'R°{index}', rule) for index, rule in enumerate(
                    self.rules) if rule.__hash__() == dupl_hash]
                result.append(dupl_rule_pack)

            raise RuleCoherenceException("duplicate rules found")

    def __str__(self):
        ret_str = f"{len(self.facts)} faits : \n [{', '.join([str(elem) for elem in self.facts])}] \n"
        ret_str = ret_str + f"{len(self.rules)} règles : \n " + \
            '\n'.join([str(rule) for rule in self.rules])
        return ret_str
