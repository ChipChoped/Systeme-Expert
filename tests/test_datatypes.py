import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import *
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
    b1 = EnumElem("test", {"hello" :Boolean("hello",True)})
    b2 = EnumElem("test", {"hello" :Boolean("hello",False)})
    assert b1.conflict(b2)

    b1 = EnumElem("test", {"hello" :Boolean("hello",True)})
    b2 = EnumElem("test", {"hello" :Boolean("hello",True)})
    assert not b1.conflict(b2)
    
    b1 = EnumElem("test", {'hello' : Boolean("hello",True)})
    b2 = EnumElem("tet", {'hello' : Boolean("hello",False)})
    assert not b1.conflict(b2)

    
    assert not b1.override(Boolean("hello",False))

    

def test_enum_equal():
    e1 = EnumElem("name", {"truc1" :Boolean("truc1", True), "truc2" : Boolean("truc2", False)})
    e2 = EnumElem("name", {"truc1" :Boolean("truc1", True), "truc2" : Boolean("truc2", False), "truc3" : Boolean("truc3", False)})

    assert e2.equal(e1)

def test_variable_type():
    assert VariableTypes.BOOLEAN != VariableTypes.NUMBER

def test_constraint_nok():
    with pytest.raises(Exception) as e_info:
        c1 = Constraint(Boolean("name", True), OperatorTypes.GREATER)

def test_constraint_bool():
    c1 = Constraint(Boolean("name", True), OperatorTypes.EQUALS)
    assert c1.str_condensed() == 'name_equal_True'
    c2 = Constraint(Boolean("name", False), OperatorTypes.EQUALS)
    assert c2.str_condensed() == 'name_equal_False'

def test_constraint_number():
    n1 = Constraint(Number("name", 3), OperatorTypes.GREATER)
    assert n1.str_condensed() == 'name_greater_3'
    n2 = Constraint(Number("name", 3), OperatorTypes.GREATER_OR_EQUAL)
    assert n2.str_condensed() == 'name_greaterOrEqual_3'

def test_contraint_bool_validity():
    c1 = Constraint(Boolean("name", True), OperatorTypes.EQUALS)
    b2 = Boolean("autre", True)
    assert c1.satisfy(b2)

    b3 = Boolean("encore_autre", False)
    assert not c1.satisfy(b3)

def test_contraint_enum_validity():
    c1 = Constraint(EnumElem("name", {"truc1" :Boolean("truc1", True), "truc2" : Boolean("truc2", False)}), OperatorTypes.EQUALS)
    assert c1.satisfy(EnumElem("name", {"truc1" :Boolean("truc1", True), "truc2" : Boolean("truc2", False), "truc3" : Boolean("truc3", False)}))

def test_contraint_number_validity():
    c1 = Constraint(Number("name", 3), OperatorTypes.EQUALS)
    c2 = Constraint(Number("name", 2), OperatorTypes.EQUALS)
    c3 = Constraint(Number("name", 2), OperatorTypes.GREATER)

    n1 = Number("autre", 3)
    assert c1.satisfy(n1)
    assert not c2.satisfy(n1)
    assert c3.satisfy(n1)

def test_constraint_satisfiable():
    c1 = Constraint(Number("name", 3), OperatorTypes.EQUALS)
    facts = {"truc" : Number("truc", 3),"name" : Number("name",3)}
    assert c1.satisfiable(facts)
    
    facts = {"truc" : Number("truc", 3),"name" : Number("name",4)}
    assert not c1.satisfiable(facts)


def test_hypothesis_satisfiable():
    c1 = Constraint(Number("name", 3), OperatorTypes.EQUALS)
    c2 = Constraint(Boolean("AutreBool", False), OperatorTypes.EQUALS)
    
    r1 = ConcreteRule([c1],[], "")
    r2 = ConcreteRule([c2],[], "")
    r3 = ConcreteRule([c1, c2],[], "")

    h1 = Hypothesis("h1", [r1, r2])
    facts = {"truc" : Number("truc", 3),"name" : Number("name",3)}
    assert h1.satisfy(facts)
    
    h2 = Hypothesis("h2", [r3])
    facts = {"truc" : Number("truc", 3),"name" : Number("name",4)}
    assert not h2.satisfy(facts)
