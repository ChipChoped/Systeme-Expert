from parser.CustomLexer import CustomLexer
from parser.ParserUtils import ParserAction
from Datatypes import Boolean, Metarule, ConcreteRule, Number, EnumElem, Constraint, OperatorTypes, Hypothesis
from Moteur import Moteur
from CoherenceExceptions import *
from ParsingException import *
import ply.yacc as yacc
import logging



class CustomParser(object):
    
    def c_load(self, file_path, *args):
        try:
            file : TextIoWrapper = open(file_path, "r")
            for line in file:
                self.parser.parse(line)
        except Exception as e:
            self.handle_generic_exception(Exception(f"Le fichier {file_path} n'existe pas"))

    def c_context(self, *args):
        print(self.moteur.context)

    def c_forward(self, hypothese_used, *args):
        print("chainage avant, avec pour but : "+str(hypothese_used))

        hypothese = self.moteur.context.hypothesis.get(hypothese_used)

        if hypothese is None:
            raise MissingArguments("L'Hypothèse entrée en paramètre n'existe pas")
    
        contexte_ajoute = self.moteur.chainageAvant(hypothese)
        print(f'Context ajouté : {contexte_ajoute}')
        

    def c_backward(self, *args):
        print("chainage arrière, avec pour hypothèses : " + str(args))
        hypotheses_vraies = self.moteur.chainageArriere(args)
        print(f'Right hypotheses : {hypotheses_vraies}')


    def p_statement_empty(self,p):
        '''statement : '''
        self.current_line+=1

    def p_statement_function(self, p):
        '''statement : fonction'''
        self.current_action = ParserAction.Function
        self.current_line+=1


    def p_statement_metaregle(self, p):
        '''statement : metaregle'''
        self.current_line+=1


    def p_statement_assignation(self, p):
        '''statement : assignation'''
        self.moteur.inputFact(p[1])   
        self.current_line+=1
        return p

    def p_statement_rule(self,p):
        ''' statement : regle '''
        self.moteur.inputRule(p[1])
        self.current_line+=1
        return p
    
    def p_statement_hypothese(self, p):
        '''statement : hypothese'''
        self.moteur.inputHypothesis(p[1])
        self.current_line+=1
        return p


    def p_fonction_arg(self, p):
        '''fonction : MOT OPEN_PAR argument CLOSE_PAR'''
        try : 
            fun = getattr(self, "c_"+p[1])
            fun(*p[3])
        except Exception as e: 
            self.handle_functionNotFound_exception(e)
    
        logging.debug(f'fonction détectée !, {p[1]}')

    def p_fonction_no_arg(self, p):
        '''fonction : MOT OPEN_PAR CLOSE_PAR'''
        try :
            fun = getattr(self, "c_"+p[1])
            fun()
        except Exception as e: 
            self.handle_functionNotFound_exception(e)

        logging.debug(f'fonction détectée !')

    def p_assignation_value(self,p):
        '''assignation : MOT EQUALS value'''
        logging.debug('assignation with value')   
        assignation = p[3]
        assignation.name = p[1]
        p[0] = assignation
        return p
 
    def p_assignation_boolean(self, p):
        '''assignation : boolean'''
        logging.debug('assignation with boolean')     
        p[0] = p[1]
        return p

    def p_enum_list_seul(self,p):
        '''enum_list : boolean'''
        p[0] = EnumElem("",{p[1].name : p[1]})
        return p

    def p_enum_list_many(self,p):
        '''enum_list : boolean COMMA enum_list'''
        p[0] = p[3]
        if not p[0].override(p[1]):
            raise FactCoherenceException(f"Cette énumération n'est pas cohérente")
        return p

    def p_enum_with_list(self,p):
        '''enum : OPEN_BRACK enum_list CLOSE_BRACK'''
        p[0] = p[2]
        return p

    def p_enum_seul(self, p):
        '''enum : boolean'''
        p[0] = EnumElem(p[1].name, {p[1].name : p[1]})
        return p

    def p_value_enum(self, p):
        '''value : enum'''
        logging.debug('enum')  
        p[0] = p[1]      
        return p

    def p_value_number(self, p):
        '''value : NUMBER'''
        logging.debug('number')
        p[0] = Number("",p[1])    
        return p

    def p_argument_seul(self, p):
        '''argument : MOT
                    | STRING'''
        p[0] = [p[1]]
        return p

    def p_comparateur_equal(self, p):
        '''comparateur : EQUALITY'''
        p[0] = OperatorTypes.EQUALS
        return p
   
    def p_comparateur_greater(self, p):
        '''comparateur : GREATER'''
        p[0] = OperatorTypes.GREATER
        return p

    def p_comparateur_greaterOrEqual(self, p):
        '''comparateur : GREATER_EQUAL'''
        p[0] = OperatorTypes.GREATER_OR_EQUAL
        return p

    def p_comparateur_less(self, p):
        '''comparateur : LESS'''
        p[0] = OperatorTypes.LESS
        return p
        
    def p_comparateur_lessOrEqual(self, p):
        '''comparateur : LESS_EQUAL'''
        p[0] = OperatorTypes.LESS_OR_EQUAL
        return p

    # def p_contrainte_neg(self, p):
    #     '''contrainte : NON contrainte'''
    #     contrainte = p[2]
    #     contrainte.positive = not contrainte.positive
    #     p[0] = contrainte
    #     return p

    def p_consequence_seul(self, p):
        '''consequence : assignation'''
        p[0] = [p[1]]
        logging.debug("consequence detected")
        return p
    
    def p_consequence_suite(self,p):
        '''consequence : assignation ET consequence'''
        p[0] = [p[1]] + p[3]
        return p

    def p_contrainte_bool(self,p):
        '''contrainte : boolean'''
        p[0] = Constraint(p[1], OperatorTypes.EQUALS)
        return p 
    
    def p_contrainte_value(self,p):
        '''contrainte : MOT comparateur value'''
        logging.debug("contrainte detected")
        value = p[3]
        value.name = p[1]
        p[0] = Constraint(value, p[2])
        return p

    def p_ensemble_arguments(self, p):
        '''argument : MOT COMMA argument'''
        p[0] = [p[1]]+p[3]
        return p

    # def p_fait(self, p):
    #     '''fait : element'''
    #     logging.debug(f'fait détecté : [{p[1]}]')
        
    #     self.moteur.inputFact(p[1])
    #     return p 

    def p_hypothese(self, p):
        '''hypothese : MOT DEUX_POINTS hypothese_contenu'''
        self.current_action.Hypothese
        p[0] = Hypothesis(p[1], p[3])
        return p[0]

    def p_hypothese_contenu_alone(self,p):
        '''hypothese_contenu : premisse'''
        logging.debug(f'Hypothèse détectée')
        p[0] = [ConcreteRule(p[1], [], "")]
        return p 
    
    def p_hypothese_contenu_mult(self, p):
        '''hypothese_contenu : premisse COMMA hypothese_contenu'''
        p[0] = [ConcreteRule(p[1], [], "")] + p[3]
        return p

    def p_regle(self, p):
        '''regle : MOT DEUX_POINTS premisse IMPLIQUE consequence'''
        self.current_action.Rule
        p[0] = ConcreteRule(p[3], p[5], p[1])
        logging.debug(f'regle détecté : {p[0]}')
        return p

        # try:
        #     self.moteur.inputRule(p[0])
        # except RuleCoherenceException as r:
        #     logging.error(r)
        #     return None
        # return p 


    def p_metaregle_exclusive_ordonne(self, p):
        '''metaregle : MOT DEUX_POINTS OPEN_BRACK liste_mots CLOSE_BRACK'''
        logging.debug(f'Metaregle détectée : {p[1]}, {p[4]}')
        self.current_action.MetaRule
        meta : Metarule
        self.moteur.createMetarule(p[1], p[4], False)
        return p

    def p_metaregle_exclusive_non_ordonnee(self, p):
        '''metaregle : MOT DEUX_POINTS OPEN_BRACK liste_mots CLOSE_BRACK OPEN_BRACK STRING CLOSE_BRACK'''
        self.current_action.MetaRule
        meta : Metarule
        self.moteur.createMetarule(p[1], p[4], True, p[7])
        return p


    def p_liste_mots_seul(self,p):
        '''liste_mots : MOT COMMA MOT'''
        p[0] = [p[1], p[3]]
        return p

    def p_liste_mots(self,p):
        '''liste_mots : MOT COMMA liste_mots'''
        p[0] = [p[1]]+p[3]
        return p

    def p_premisse_mult(self, p):
        'premisse : contrainte ET premisse'

        p[0] = [p[1]] + p[3]
        logging.debug('premisse mult détectée ')
        return p 

    def p_premisse_seul(self, p):
        'premisse : contrainte'
        p[0] = [p[1]]
        logging.debug('premisse seule détecté ')
        return p 

    def p_boolean_negative(self, p):
        '''boolean : NON MOT'''

        p[0] = Boolean(p[2], False)
        # logging.debug(f'element negatif [{p[2]}] detecte')
        return p

    def p_boolean(self, p):
        'boolean : MOT'
        
        p[0] = Boolean(p[1], True)
        # logging.debug(f'element positif [{p[1]}] detecte')
        return p

    def p_error(self, p):
        self.handle_parsing_exception()

    def __init__(self, moteur : Moteur):
        self.tokens = CustomLexer.tokens
        self.moteur = moteur
        self.parser = yacc.yacc(module=self)
        self.current_action : ParserAction = ParserAction.Default
        self.current_line : int =  1


    def handle_rule_coherence_exception(self, exception : RuleCoherenceException):
        self.messageLigne()
        print("Exception de cohérence de rêgle")
    

    def handle_functionNotFound_exception(self, exception):
        self.messageLigne()
        print("Cette fonction n'existe pas")


    def handle_parsing_exception(self):
        self.messageLigne()
        print(f"Erreur de parsing, appelez la fonction help() pour un rappel des syntaxes")
        self.current_line += 1
    
    def handle_generic_exception(self, exception : Exception):
        self.messageLigne()
        print(str(exception))

    def messageLigne(self):
        print(f"ERREUR LIGNE : {self.current_line}")
