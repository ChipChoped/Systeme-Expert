from Datatypes import Element, Rule, ConcreteRule
from Context import Context
import copy

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

    #crée une metaregle à partir de son nom et du nom de ses rêgles
    def createMetarule(self, rule_name : str, rule_list : list[str], sorted : bool = True):
        self.context.addMetarule(rule_name, rule_list, sorted)

    #sature les rêgles afin de déduire la plus grande base de faits possible
    def chainageAvant(self, objectives : list[Element] = []):
        regles_utilises : list[Rule] = list()
        faits_ajoutes : list[Fact] = list()
        # return_context : Context = Context()
        
        # objectives = [Element(objective, True) for objective in objectives]

        simulation_context : Context = copy.deepcopy(self.context)

        res = True
        while simulation_context.rules.values() != [] and res and not any([objective in list(simulation_context.facts.values()) for objective in objectives]):
            ajout  = Moteur.trouverCorrespondanceRegle(simulation_context.facts ,list(simulation_context.rules.values()))
            if ajout is None:
                res = False
            else :
                # [self.context.addFact(f) for f in ajout_regle[1]]
                print("ajout : " + str(ajout))
                faits_ajoutes.extend(ajout[0].consequence)
                [simulation_context.addFact(fact) for fact in ajout[0].consequence]
                simulation_context.rules.pop(ajout[1])
                regles_utilises.append(ajout[0])

        return (faits_ajoutes, regles_utilises)

    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegle(base_de_faits : list[Element], base_de_regles : list[Rule]) -> 'ConcreteRule | None':
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

        for hypothesis in hypotheses:
            for rule in list(simulation_context.rules.values()):
                returned_rule = rule.concludes(hypothesis)
                if returned_rule:
                    for fact in list(simulation_context.facts.values()):
                        if fact.conflicts(returned_rule[0].consequence):
                            break

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
