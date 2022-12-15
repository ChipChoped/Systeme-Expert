from Datatypes import Element, Rule, ConcreteRule, Hypothesis, VariableTypes, Constraint, EnumElem
from Context import Context
import logging
import copy
from typing import Optional


# TODO : résoudre le cassage du chainage avant

class Moteur(object):

    def __init__(self, context: Context):
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

    def inputHypothesis(self, hypothese: Hypothesis):
        self.context.addHypothesis(hypothese)

    #crée une metaregle à partir de son nom et du nom de ses rêgles
    def createMetarule(self, rule_name : str, rule_list : list[str], ordered : bool = False, order_type : str = ""):
        self.context.addMetarule(rule_name, rule_list, ordered, order_type)

    # sature les rêgles afin de déduire la plus grande base de faits possible
    def chainageAvant(self, objectives: Hypothesis) -> Context:

        if objectives is None:
            logging.warning("No objective was given")
            objectives = Hypothesis("default",
                                    [Constraint(Boolean("unsatisfiable_default_constraint", True), VariableTypes)])

        return_context: Context = Context()

        simulation_context: Context = copy.deepcopy(self.context)
        # print("simulation context :")
        # print(simulation_context)
        # print("return_context :")
        # print(return_context)

        res = True
        while simulation_context.rule_list != [] and res and not objectives.satisfy(simulation_context.facts):
            ajout  = Moteur.trouverCorrespondanceRegle(simulation_context.facts ,simulation_context.rule_list)
            if ajout is None:
                res = False
            else:
                [(simulation_context.addFact(copy.copy(fact)), return_context.addFact(copy.copy(fact))) for fact in
                 ajout[0].consequence]
                return_context.addRule(ajout[0])
                simulation_context.removeRule(ajout[1])
            
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

    def satisfaction_regle(base_de_faits: list, regle: Rule):
        for element in regle.premisse:
            if element in base_de_faits:
                continue
            else:
                return False
        return True

    def chainageArriere(self, hypotheses_: Hypothesis) -> list[tuple[Constraint, Context, bool]]:
        i = 1
        hypotheses: list[Constraint] = []
        return_context: list[tuple[Constraint, Context, bool]] = []

        for rule in hypotheses_.rules:
            hypotheses.append(rule.premisse[0])

        # liste les hypothèses
        for hypothesis in hypotheses:
            context = self.recChainageArriere(hypothesis, (Context(), True))
            return_context.append((hypothesis, context[0], context[1]))

        return return_context

    def recChainageArriere(self, hypothesis: Constraint, return_context: tuple[Context, bool]) -> tuple[Context, bool]:
        found_rule = self.trouverRegleConcluante(
            hypothesis, list(self.context.facts.values()), list(self.context.rules.values()))

        if found_rule:
            true_hypothesis = True
            for premisse in found_rule[0].premisse:
                # if list(self.context.facts.values()).count(premisse.elem) == 0:
                if not self.faitConnu(premisse.elem, list(self.context.facts.values())):
                    return_context = self.recChainageArriere(premisse, return_context)
                    if not return_context[1]:
                        true_hypothesis = False
                        break

            if true_hypothesis:
                for premisse in found_rule[0].premisse:
                    return_context[0].addFact(premisse.elem)
                return_context[0].addRule(found_rule[0])

                return return_context[0], True

        return return_context[0], False

    def faitConnu(self, researched_fact: Element, facts: [Element]):
        for fact in facts:
            if fact.equal(researched_fact):
                return True

        return False

    def trouverRegleConcluante(self, hypothesis: Constraint, facts: list[Element], rules: list[Rule]):
        """Match rule"""
        for rule in rules:
            found_rule = rule.concludes(hypothesis.elem)
            if found_rule:
                conflict = False
                for fact in facts:
                    if fact.conflicts(found_rule[0].consequence):
                        conflict = True

                if not conflict:
                    for premisse in found_rule[0].premisse:
                        if premisse.elem.conflicts(list(self.context.facts.values())):
                            conflict = True

                if not conflict:
                    return found_rule

        return None
