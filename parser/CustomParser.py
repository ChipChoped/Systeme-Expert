from parser.CustomLexer import CustomLexer
from CoherenceExceptions import RuleCoherenceException
from Datatypes import Boolean, Metarule, ConcreteRule, Number, EnumElem
from Moteur import Moteur
import ply.yacc as yacc
import logging



class CustomParser(object):
    
    def c_load(self, file_path, *args):
        file : TextIoWrapper = open(file_path, "r")
        for line in file:
            self.parser.parse(line)

    def c_context(self, *args):
        print(self.moteur.context)

    def c_forward(self, *args):
        print("chainage avant, avec pour but : "+str(args))
        faits_ajoutes, regles_utilises = self.moteur.chainageAvant(args)
        print(f'Added facts : {faits_ajoutes}, used rules : {regles_utilises}')

    def c_backward(self, *args):
        print("chainage arrière, avec pour hypothèses : " + str(args))
        hypotheses_vraies = self.moteur.chainageArriere(args)
        print(f'Right hypotheses : {hypotheses_vraies}')

    def p_statement(self, p):
        '''statement : regle
                    | assignation
                    | fonction
                    | metaregle'''         

    def p_fonction_arg(self, p):
        '''fonction : MOT OPEN_PAR argument CLOSE_PAR'''
        logging.debug(f'fonction détectée !, {p[1]}')
        fun = getattr(self, "c_"+p[1])
        fun(*p[3])
    
    def p_fonction_no_arg(self, p):
        '''fonction : MOT OPEN_PAR CLOSE_PAR'''
        fun = getattr(self, "c_"+p[1])
        fun()

        logging.debug(f'fonction détectée !')

    def p_assignation_value(self,p):
        '''assignation : MOT EQUALS value'''
        logging.debug('assignation with value')   
        p[3].name = p[1]
        self.moteur.inputFact(p[3])     
        return p
 
    def p_assignation_boolean(self, p):
        '''assignation : boolean'''
        logging.debug('assignation with boolean')     
        self.moteur.inputFact(p[1])   
        return p

    def p_value_enum(self, p):
        '''value : MOT'''
        logging.debug('enum')  
        p[0] = EnumElem("",p[1])      
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

    def p_arguments_ordonnes(self, p):
        '''ordonnes : MOT GREATER ordonnes'''
        p[0] = [p[1]]+p[3]
        return p

    def p_argument_ordonne_seul(self, p):
        '''ordonnes : MOT '''
        p[0] = [p[1]]
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

    def p_regle(self, p):
        '''regle : MOT DEUX_POINTS premisse IMPLIQUE premisse'''
        p[0] = ConcreteRule(p[3], p[5], p[1])
        logging.debug(f'regle détecté : {p[0]}')

        try:
            self.moteur.inputRule(p[0])
        except RuleCoherenceException as r:
            logging.error(r)
            return None
        return p 


    def p_metaregle_ordonne(self, p):
        '''metaregle : MOT DEUX_POINTS OPEN_BRACK ordonnes CLOSE_BRACK'''
        logging.debug(f'Metaregle détectée : {p[1]}, {p[4]}')
        meta : Metarule
        self.moteur.createMetarule(p[1], p[4], True)
        return p

    def p_premisse_mult(self, p):
        'premisse : boolean ET premisse'

        p[0] = [p[1]] + p[3]
        logging.debug('premisse mult détectée ')
        return p 

    def p_premisse_seul(self, p):
        'premisse : boolean'
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
        print("Syntax error in input!")
        print(p)

    def __init__(self, moteur : Moteur):
        self.tokens = CustomLexer.tokens
        self.moteur = moteur
        self.parser = yacc.yacc(module=self)

