from Moteur import Moteur
from Datatypes import Element, Rule
from CoherenceExceptions import RuleCoherenceException
import logging
import collections


class Context(object):

    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, fact: Element):
        self.facts.append(fact)
        self.facts = Moteur.chainageAvant(self.facts, self.rules)

    def addRule(self, rule: Rule):
        self.rules.append(rule)
        try:
            self.checkRulesCoherence()
            self.facts = Moteur.chainageAvant(self.facts, self.rules)
            
        except RuleCoherenceException as r:
            logging.error(r)
            self.rules.pop()

    def checkFactBaseCoherence(self):
        pass

    def checkRulesCoherence(self):
        self.checkRulesNoDuplicates()

    def checkRulesNoDuplicates(self):

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
