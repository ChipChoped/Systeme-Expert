from Datatypes import Element, Rule, ConcreteRule, Hypothesis, VariableTypes
from Context import Context
import logging
import copy
from typing import Optional

#TODO : résoudre le cassage du chainage avant

class Moteur(object):

    def __init__(self, context : Context):
        self.context = context

    def inputFact(self, fact: Element):
        self.context.addFact(fact)
        # self.saturateBase()

    def inputRule(self, rule: Rule):
        self.context.addRule(rule)
        # try:
        #     self.context.checkRulesCoherence()
        #     self.saturateBase()
        # except RuleCoherenceException as r:
        #     logging.error(r)
        #     self.rules.pop()

    def inputHypothesis(self, hypothese : Hypothesis):
        self.context.addHypothesis(hypothese)

    #crée une metaregle à partir de son nom et du nom de ses rêgles
    def createMetarule(self, rule_name : str, rule_list : list[str], sorted : bool = True):
        self.context.addMetarule(rule_name, rule_list, sorted)

    #sature les rêgles afin de déduire la plus grande base de faits possible
    def chainageAvant(self, objectives : Hypothesis) -> Context:

        if objectives is None : 
            logging.warning("No objective was given")
            objectives = Hypothesis("default", [Constraint(Boolean("unsatisfiable_default_constraint", True), VariableTypes)])


        return_context : Context = Context()

        simulation_context : Context = copy.deepcopy(self.context)
        # print("simulation context :")
        # print(simulation_context)
        # print("return_context :")
        # print(return_context)

        res = True
        while simulation_context.rules.values() != [] and res and not objectives.satisfy(simulation_context.facts):
            ajout  = Moteur.trouverCorrespondanceRegle(simulation_context.facts ,list(simulation_context.rules.values()))
            if ajout is None:
                res = False
            else :
                [(simulation_context.addFact(copy.copy(fact)) , return_context.addFact(copy.copy(fact))) for fact in ajout[0].consequence]
                return_context.addRule(ajout[0])
                simulation_context.rules.pop(ajout[1])
            
            # print("simulation context :")
            # print(simulation_context)
            # print("return_context :")
            # print(return_context)

        return return_context

    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegle(base_de_faits : list[Element], base_de_regles : list[Rule]) -> Optional[tuple[ConcreteRule, str]]:
        """Match rule"""
        for regle in base_de_regles:
            ret = regle.satisfy(base_de_faits)
            if ret:
                return ret
        return None

   
    def satisfaction_regle(base_de_faits : list, regle : Rule):
        for element in regle.premisse:
            if element in base_de_faits:
                continue
            else:
                return False
        return True


    def chainageArriere(self, hypotheses : list[str]):
        right_hypotheses = []
        hypotheses = [Element(hypothesis, True) for hypothesis in hypotheses]

        simulation_context: Context = copy.deepcopy(self.context)

        # liste les hypothèses
        for hypothesis in hypotheses:
            #liste les rêgles
            for rule in list(simulation_context.rules.values()):
                # recherche de rêgle concluante 
                returned_rule = rule.concludes(hypothesis)
                if returned_rule:
                    # recherche de conflits avec la base de connaissances virtuelle
                    for fact in list(simulation_context.facts.values()):
                        if fact.conflicts(returned_rule[0].consequence):
                            break
                        
                        # application de la rêgle
                        applicable_rule = True

                        for premisse in returned_rule[0].premisse:
                            if premisse.conflicts(list(simulation_context.facts.values())):
                                applicable_rule = False

                        if applicable_rule:
                            true_hypothesis = True
                            for premisse in returned_rule[0].premisse:
                                if list(simulation_context.facts.values()).count(premisse) == 0:
                                    if not self.chainageArriere([premisse.name]):
                                        true_hypothesis = False
                                        break

                            if true_hypothesis:
                                right_hypotheses.append(hypothesis)
                                break

        return right_hypotheses
