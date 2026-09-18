#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration complète de l'analyseur d'erreurs
Montre toutes les fonctionnalités du chatbot
"""

from error_analyzer import ErrorAnalyzerChatbot

print("=" * 80)
print("🎯 DÉMONSTRATION DE L'ANALYSEUR D'ERREURS DE PROGRAMMATION")
print("=" * 80)

analyzer = ErrorAnalyzerChatbot()

# Démonstration 1: Analyse d'erreurs Python multiples
print("\n📌 Démonstration 1: Analyse de différentes erreurs Python")
print("-" * 80)

errors = [
    ("ZeroDivisionError", """Traceback (most recent call last):
  File "calc.py", line 10, in <module>
    result = total / count
ZeroDivisionError: division by zero"""),
    
    ("NameError", """Traceback (most recent call last):
  File "app.py", line 5, in <module>
    print(username)
NameError: name 'username' is not defined"""),
    
    ("IndexError", """Traceback (most recent call last):
  File "data.py", line 3, in <module>
    item = items[5]
IndexError: list index out of range"""),
]

for error_name, error_report in errors:
    print(f"\n🔸 {error_name}")
    results = analyzer.analyze_error_report(error_report)
    if results:
        r = results[0]
        print(f"   Explication: {r['explanation'][:60]}...")
        print(f"   Solutions: {len(r['solutions'])} proposées")

# Démonstration 2: Détails complets d'une erreur
print("\n\n📌 Démonstration 2: Analyse détaillée d'une erreur")
print("-" * 80)

detailed_error = """Traceback (most recent call last):
  File "convert.py", line 15, in process_data
    number = int(user_input)
ValueError: invalid literal for int() with base 10: 'hello'"""

results = analyzer.analyze_error_report(detailed_error)
for result in results:
    print(f"\n🔍 Type: {result['error_type']}")
    print(f"📁 Fichier: {result['file']}")
    print(f"📍 Ligne: {result['line']}")
    print(f"💻 Code: {result['code_snippet']}")
    print(f"\n💡 Explication: {result['explanation']}")
    print(f"\n🔍 Causes possibles:")
    for cause in result['causes_possibles']:
        print(f"   • {cause}")
    print(f"\n✅ Solutions:")
    for solution in result['solutions']:
        print(f"   • {solution}")

# Démonstration 3: Analyse depuis fichiers
print("\n\n📌 Démonstration 3: Analyse de fichiers d'erreurs")
print("-" * 80)

import os
example_files = [f for f in os.listdir('examples') if f.endswith('.txt')]
print(f"\n📂 Fichiers disponibles: {len(example_files)}")
for file in example_files[:2]:  # Analyser les 2 premiers
    filepath = os.path.join('examples', file)
    results = analyzer.analyze_from_file(filepath)
    if results:
        print(f"\n   ✓ {file}: {results[0]['error_type']}")

# Démonstration 4: Export JSON
print("\n\n📌 Démonstration 4: Export des résultats")
print("-" * 80)

analyzer.export_analysis(results, "/tmp/demo_analysis.json")

import json
with open("/tmp/demo_analysis.json", "r") as f:
    exported = json.load(f)
    print(f"\n✓ Exporté {len(exported)} analyse(s)")
    print(f"✓ Champs exportés: {', '.join(exported[0].keys())}")

# Statistiques finales
print("\n\n" + "=" * 80)
print("📊 STATISTIQUES")
print("=" * 80)
print(f"✓ Types d'erreurs dans la base: {len(analyzer.chatbot.error_database)}")
print(f"✓ Langages supportés: Python, JavaScript, Java")
print(f"✓ Modes d'utilisation: Interactif, Fichier, Programmatique")
print(f"✓ Export: JSON")
print("\n✅ Démonstration terminée avec succès!")
