from CustomLexer import CustomLexer
from CustomParser import CustomParser

if __name__ == '__main__':
    print("test du lexer, entrez ce que vous voulez !")
    prompt = input()
    lexer = CustomLexer.generateLexer()
    lexer.input(prompt)
    for lex_res in lexer:
        print(lex_res)
    
    print("parsing : ")
    parser = CustomParser.generateParser()
    result = parser.parse(prompt)
    