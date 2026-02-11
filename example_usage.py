#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation de l'analyseur d'erreurs
"""

from error_analyzer import ErrorAnalyzerChatbot

# Créer l'analyseur
analyzer = ErrorAnalyzerChatbot()

# Exemple 1: Analyser une erreur simple
print("=" * 70)
print("Exemple 1: Analyse d'un NameError")
print("=" * 70)

error_report = """
Traceback (most recent call last):
  File "main.py", line 15, in <module>
    print(username)
NameError: name 'username' is not defined
"""

results = analyzer.analyze_error_report(error_report)
for result in results:
    print(f"\n📋 Type d'erreur: {result['error_type']}")
    print(f"💬 Message: {result['message']}")
    print(f"\n📖 Explication: {result['explanation']}")
    print(f"\n✅ Solutions:")
    for i, solution in enumerate(result['solutions'], 1):
        print(f"   {i}. {solution}")

# Exemple 2: Analyser depuis un fichier
print("\n\n" + "=" * 70)
print("Exemple 2: Analyse depuis un fichier")
print("=" * 70)

results = analyzer.analyze_from_file("examples/error_python_3.txt")
if results:
    result = results[0]
    print(f"\n📋 Type d'erreur: {result['error_type']}")
    print(f"📁 Fichier: {result['file']}")
    print(f"📍 Ligne: {result['line']}")
    print(f"\n✅ Solutions:")
    for solution in result['solutions']:
        print(f"   • {solution}")

# Exemple 3: Export JSON
print("\n\n" + "=" * 70)
print("Exemple 3: Export en JSON")
print("=" * 70)

analyzer.export_analysis(results, "/tmp/error_analysis.json")
print("\n✅ Analyse exportée dans /tmp/error_analysis.json")

# Lire et afficher le JSON
import json
with open("/tmp/error_analysis.json", "r") as f:
    data = json.load(f)
    print(f"\nContenu JSON (extrait):")
    print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500] + "...")
