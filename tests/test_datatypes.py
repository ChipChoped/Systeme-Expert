import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule, Boolean, Number, EnumElem, VariableTypes
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser



# @pytest.fixture
# def base_context():
#     moteur = Moteur(Context())
#     lexer = CustomLexer().lexer
#     custom = CustomParser(moteur)
#     return custom


def test_boolean_conflict():
    b1 = Boolean("test", True)
    b2 = Boolean("test", False)
    assert b1.conflict(b2)

    b1 = Boolean("test", True)
    b2 = Boolean("test", True)
    assert not b1.conflict(b2)
   
    b1 = Boolean("tst", True)
    b2 = Boolean("test", True)
    assert not b1.conflict(b2)

def test_boolean_conflicts():
    b1 = Boolean("test", True)
    assert b1.conflicts([Boolean('a', False), Boolean('b', True), Boolean('test', False)])
    assert not b1.conflicts([Boolean('a', False), Boolean('b', True)])

def test_number_conflict():
    b1 = Number("test", 2)
    b2 = Number("test", 3)
    assert b1.conflict(b2)

    b1 = Number("test", 2)
    b2 = Number("test", 2)
    assert not b1.conflict(b2)
   
    b1 = Number("test", 2)
    b2 = Number("tet", 2)
    assert not b1.conflict(b2)

def test_enum_conflict():
    b1 = EnumElem("test", "hello")
    b2 = EnumElem("test", "hella")
    assert b1.conflict(b2)

    b1 = EnumElem("test", "salut")
    b2 = EnumElem("test", "salut")
    assert not b1.conflict(b2)
    
    b1 = EnumElem("test", "salut")
    b2 = EnumElem("tet", "hello")
    assert not b1.conflict(b2)

def test_variable_type():
    assert VariableTypes.BOOLEAN != VariableTypes.NUMBER