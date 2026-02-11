#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'analyseur d'erreurs
"""

from error_analyzer import ErrorAnalyzerChatbot

def test_python_errors():
    """Test l'analyse d'erreurs Python"""
    analyzer = ErrorAnalyzerChatbot()
    
    print("=" * 70)
    print("Test 1: ZeroDivisionError")
    print("=" * 70)
    
    error1 = """Traceback (most recent call last):
  File "test.py", line 5, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero"""
    
    results = analyzer.analyze_error_report(error1)
    assert len(results) == 1
    assert results[0]['error_type'] == 'ZeroDivisionError'
    print(f"✅ Type d'erreur correctement détecté: {results[0]['error_type']}")
    print(f"✅ Explication: {results[0]['explanation']}")
    print(f"✅ Nombre de solutions: {len(results[0]['solutions'])}")
    
    print("\n" + "=" * 70)
    print("Test 2: NameError")
    print("=" * 70)
    
    error2 = """Traceback (most recent call last):
  File "app.py", line 10, in <module>
    print(undefined_variable)
NameError: name 'undefined_variable' is not defined"""
    
    results = analyzer.analyze_error_report(error2)
    assert len(results) == 1
    assert results[0]['error_type'] == 'NameError'
    print(f"✅ Type d'erreur correctement détecté: {results[0]['error_type']}")
    print(f"✅ Fichier détecté: {results[0]['file']}")
    print(f"✅ Ligne détectée: {results[0]['line']}")
    
    print("\n" + "=" * 70)
    print("Test 3: ValueError")
    print("=" * 70)
    
    error3 = """Traceback (most recent call last):
  File "convert.py", line 3, in <module>
    num = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'"""
    
    results = analyzer.analyze_error_report(error3)
    assert len(results) == 1
    assert results[0]['error_type'] == 'ValueError'
    print(f"✅ Type d'erreur correctement détecté: {results[0]['error_type']}")
    print(f"✅ Message: {results[0]['message']}")
    
    print("\n" + "=" * 70)
    print("Test 4: IndexError")
    print("=" * 70)
    
    error4 = """Traceback (most recent call last):
  File "lists.py", line 2, in <module>
    value = my_list[100]
IndexError: list index out of range"""
    
    results = analyzer.analyze_error_report(error4)
    assert len(results) == 1
    assert results[0]['error_type'] == 'IndexError'
    print(f"✅ Type d'erreur correctement détecté: {results[0]['error_type']}")
    
    print("\n" + "=" * 70)
    print("Test 5: Chatbot")
    print("=" * 70)
    
    response = analyzer.chatbot.chat("bonjour")
    assert "assistant" in response.lower() or "aide" in response.lower()
    print(f"✅ Chatbot répond correctement: {response[:80]}...")
    
    response = analyzer.chatbot.chat("aide")
    assert "aide" in response.lower() or "help" in response.lower()
    print(f"✅ Chatbot fournit l'aide: {response[:80]}...")
    
    print("\n" + "=" * 70)
    print("✅ TOUS LES TESTS ONT RÉUSSI!")
    print("=" * 70)

if __name__ == "__main__":
    test_python_errors()
