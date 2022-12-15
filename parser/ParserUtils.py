from enum import Enum

class ParserAction(Enum):
    Rule = 0
    Hypothese = 1
    Function = 2
    Assignation = 3
    MetaRule = 4
    Default = 5