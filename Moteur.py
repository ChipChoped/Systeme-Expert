from Datatypes import Rule
import logging

class Moteur(object):

    #renvoie une base de fait déduite des rêgles
    #sature les rêgles pour l'instant
    def chainageAvant(base_de_faits : list, base_de_regles : list)->list:
        res = True
        while base_de_regles != [] and res:
            ajout_regle = Moteur.trouverCorrespondanceRegle(base_de_faits, base_de_regles)
            if ajout_regle is None:
                res = False
            else :
                base_de_faits += ajout_regle[1]
                base_de_regles.pop(ajout_regle[0])
        return base_de_faits

    # cherche une rêgle afin d'étendre la base de faits
    # renvoie un tuple (index_regle, [faits_deduits]) ou None
    def trouverCorrespondanceRegle(base_de_faits : list, base_de_regles : list) -> tuple | None:
        for index, regle  in enumerate(base_de_regles):
            if Moteur.satisfaction_regle(base_de_faits, regle):
                return (index, regle.consequence)
        return None

   
    def satisfaction_regle(base_de_faits : list, regle : Rule):
        for element in regle.premisse:
            if element in base_de_faits:
                continue
            else:
                return False
        return True