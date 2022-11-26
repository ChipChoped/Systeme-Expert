from parser.CustomLexer import CustomLexer, reserved
from Datatypes import Context, Element, Rule

import ply.yacc as yacc
import logging



class CustomParser(object):
    def c_load(self, file_path, *args):
        """imparfait : ne peut pas prendre de caractères spéciaux
        à cause des limitations actuelles du parser"""
        file: TextIoWrapper = open(file_path, "r")
        for line in file:
            self.parser.parse(line)

    def p_statement(self, p):
        '''statement : regle
                    | fait
                    | hypothese
                    | fonction'''

    def p_fonction_arg(self, p):
        '''fonction : MOT OPEN_PAR argument CLOSE_PAR'''
        fun = getattr(self, "c_" + p[1])
        fun(*p[3])
        logging.debug(f'fonction détectée !')

    def p_fonction_no_arg(self, p):
        '''fonction : MOT OPEN_PAR CLOSE_PAR'''
        fun = getattr(self, "c_" + p[1])
        fun()

        logging.debug(f'fonction détectée !')

    def p_argument_seul(self, p):
        '''argument : MOT'''
        p[0] = [p[1]]
        return p

    def p_ensemble_arguments(self, p):
        '''argument : MOT COMMA argument'''
        p[0] = p[1] + p[3]
        return p

    def p_fait(self, p):
        '''fait : element'''

        logging.debug(f'fait détecté : [{p[1]}]')
        
        self.context.addFact(p[1])
        return p 

    def p_regle(self, p):
        '''regle : premisse IMPLIQUE premisse'''

        p[0] = Rule(p[1], p[3])
        logging.debug(f'regle détecté : {p[0]}')
        self.context.addRule(p[0])
        return p

    def p_hypotheses(self, p):
        '''hypothese : HYP element'''

        logging.debug(f'Hypothèse détectée')

        self.context.addHypothesis(p[2])
        return p

    def p_premisse_mult(self, p):
        'premisse : element ET premisse'

        p[0] = [p[1]] + p[3]
        # logging.debug('premisse mult détectée ')
        return p

    def p_premisse_seul(self, p):
        'premisse : element'
        p[0] = [p[1]]
        # logging.debug('premisse seule détecté ')
        return p

    def p_element_negative(self, p):
        '''element : NON MOT'''

        p[0] = Element(p[2], False)
        # logging.debug(f'element negatif [{p[2]}] detecte')
        return p

    def p_element(self, p):
        'element : MOT'

        p[0] = Element(p[1], True)
        # logging.debug(f'element positif [{p[1]}] detecte')
        return p

    def __init__(self, context : Context):
        self.tokens = CustomLexer.tokens
        self.context = context
        self.parser = yacc.yacc(module=self)