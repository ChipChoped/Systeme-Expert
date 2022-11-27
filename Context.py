from Datatypes import Element, Rule, Metarule, ConcreteRule
from CoherenceExceptions import RuleCoherenceException, FactCoherenceException
import logging
import collections


class Context(object):

    def __init__(self):
        self.facts : dict[Element] = dict()
        self.rules : dict[Rule] = dict()

    def addFact(self, fact : Element):
        check_fact : Element | None = self.facts.get(fact.name) 
        if check_fact and check_fact.positive != fact.positive:
            raise FactCoherenceException(f'{fact.name} is True and False at the same time !')
        self.facts[fact.name] = fact

#TODO : Améliorer la détection de double règles, même dans les métarègles !!
    def addRule(self, rule: ConcreteRule):
        if rule in self.rules.values():
            raise RuleCoherenceException("duplicate rules found")
        self.rules[rule.name] = rule
    
    def addMetarule(self, meta_rule_name : str, rule_list : list[str], sorted : bool = True):
        concrete_rule_list : list[ConcreteRule] = list()
        if self.rules.get(meta_rule_name): # si écrasement de la rêgle...
            logging.debug("ecrasement")
            for rule in self.rules.get(meta_rule_name).rule_list:
                self.rules[rule.name] = rule
            self.rules.pop(meta_rule_name) 

        for rule_name in rule_list :
            concrete_rule_list.append(self.rules.get(rule_name))
        
        meta_rule : Metarule = Metarule(meta_rule_name, concrete_rule_list, sorted)
        if meta_rule in self.rules.values():
            raise RuleCoherenceException("duplicate meta rule found")
        self.rules[meta_rule_name] = meta_rule
        [self.rules.pop(rule_name) for rule_name in rule_list]


    
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
        ret_str = f"{len(self.facts)} faits : \n[{', '.join([str(elem) for elem in self.facts.values()])}] \n"
        ret_str = ret_str + f"{len(self.rules)} règles : \n" + \
            '\n'.join([str(rule) for rule in self.rules.values()])
        return ret_str
