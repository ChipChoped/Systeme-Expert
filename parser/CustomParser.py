from CustomLexer import tokens
import ply.yacc as yacc

class CustomParser(object):
    def generateParser():
        
        def p_statement(p):
            '''statement : regle
                        | fait'''         

        def p_fait(p):
            '''fait : element'''
            print("fait détecté")
            return p 

        def p_regle(p):
            '''regle : premisse IMPLIQUE premisse'''
            print('regle détecté ')
            return p 

        def p_premisse_mult(p):
            'premisse : element ET premisse'
            p[0] = {'elems' :  [p[1]] + p[3]['elems'] }
            print('premisse mult détectée ')
            print(p[0])
            return p 

        def p_premisse_seul(p):
            'premisse : element'
            p[0] = {'elems' : [p[1]] }
            print('premisse seule détecté ')
            return p 

        def p_element_negative(p):
            '''element : NON MOT'''

            p[0] = { 'pos' :  False , 'name' : p[2]}
            print('element negatif detecte')
            return p

        def p_element(p):
            'element : MOT'
            p[0] = {'pos':  True, 'name' : p[1]}
            print('element positif detecté')
            return p

        return yacc.yacc()
