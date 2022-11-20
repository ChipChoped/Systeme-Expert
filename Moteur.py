from __future__ import annotations

from Datatypes import *


class Moteur(object):
    def chainageArriere(self, facts : list[Element], rules : list[Rule], hypotheses : list[Hypothesis])->list[Hypothesis]:
        right_hypotheses = []

        for hypothesis in hypotheses:
            rule_found = False

            for rule in rules:
                for consequence in rule.consequence:
                    if hypothesis == consequence:
                        rule_found = True

                    for fact in facts:
                        if fact.conflict(consequence):
                            rule_found = False
                            break

                if rule_found:
                    applicable_rule = True

                    for premisse in rule.premisse:
                        if premisse.conflicts(facts):
                            applicable_rule = False

                    if applicable_rule:
                        false_hypothesis = False
                        for premisse in rule.premisse:
                            if facts.count(premisse) == 0:
                                if not self.chainageArriere(facts, rules, premisse):
                                    false_hypothesis = True
                                    break

                        if not false_hypothesis:
                            right_hypotheses.append(hypothesis)
                            break


        return right_hypotheses


    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegleArriere(self, facts: list[Element], rules: list[Rule], hypothesis : Hypothesis) -> tuple | None:
        pass


    #renvoie une base de fait déduite des rêgles
    #sature les rêgles pour l'instant
    def chainageAvant(self, base_de_faits : list, base_de_regles : list)->list:
        res = True
        while base_de_regles != [] | res:
            pass


    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegle(self, base_de_faits : list, base_de_regles : list) -> tuple | None:
        pass