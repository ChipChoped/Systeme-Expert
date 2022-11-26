from Datatypes import Element, Rule
from CoherenceExceptions import RuleCoherenceException
from Context import Context
import logging

class Moteur(object):

    def __init__(self, context : Context):
        self.context = context

    def inputFact(self, fact: Element):
        self.context.addFact(fact)
        self.saturateBase()

    def inputRule(self, rule: Rule):
        self.context.addRule(rule)
        try:
            self.context.checkRulesCoherence()
            self.saturateBase()
        except RuleCoherenceException as r:
            logging.error(r)
            self.rules.pop()

    #sature les rêgles afin de déduire la plus grande base de faits possible
    def saturateBase(self):
        res = True
        base_de_regles : list[Regle] = self.context.rules.copy()
        while base_de_regles != [] and res:
            ajout_regle = self.trouverCorrespondanceRegle()
            if ajout_regle is None:
                res = False
            else :
                [self.context.addFact(f) for f in ajout_regle[1]]
                base_de_regles.pop(ajout_regle[0])

    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegle(self) -> tuple | None:
        """Match rule"""
        for index, regle  in enumerate(self.context.rules):
            if Moteur.satisfaction_regle(self.context.facts, regle):
                return (index, regle.consequence)
        return None

   
    def satisfaction_regle(base_de_faits : list, regle : Rule):
        for element in regle.premisse:
            if element in base_de_faits:
                continue
            else:
                return False
        return True
