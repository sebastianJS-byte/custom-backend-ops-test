import pytest

def test_suma():
    """Test simple de suma"""
    assert 2 + 2 == 4

def test_resta():
    """Test simple de resta"""
    assert 10 - 5 == 5

def test_string():
    """Test simple de string"""
    resultado = "hola" + " mundo"
    assert resultado == "hola mundo"