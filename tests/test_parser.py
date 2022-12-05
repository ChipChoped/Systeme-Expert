import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule , EnumElem, Boolean
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser



@pytest.fixture
def base_context():
    moteur = Moteur(Context())
    lexer = CustomLexer().lexer
    custom = CustomParser(moteur)
    return custom


def test_assignation(base_context):
    base_context.parser.parse("a = [test, NON truc]")
    base_context.moteur.context.facts['a'] == EnumElem('a', [Boolean('test', True), Boolean('truc', False)])

def test_assignation_enum(base_context):
    base_context.parser.parse("a = test")
    base_context.parser.parse("a = NON test2")
    base_context.moteur.context.facts['a'] == EnumElem('a', [Boolean('test', True), Boolean('test2', False)])
