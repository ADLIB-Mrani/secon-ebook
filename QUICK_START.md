# 🚀 Guide de Démarrage Rapide - Analyseur d'Erreurs

## Installation et Utilisation en 3 Étapes

### 1️⃣ Cloner le Projet
```bash
git clone https://github.com/ADLIB-Mrani/secon-ebook.git
cd secon-ebook
```

### 2️⃣ Tester l'Analyseur
```bash
# Lancer les tests
python test_error_analyzer.py

# Voir la démonstration complète
python demo.py

# Tester avec un exemple
python error_analyzer.py examples/error_python_1.txt
```

### 3️⃣ Utiliser le Chatbot
```bash
# Mode interactif
python error_analyzer.py

# Puis coller votre erreur, exemple:
# Traceback (most recent call last):
#   File "test.py", line 5
#     print(x
# SyntaxError: unexpected EOF while parsing
```

## 📝 Exemples d'Utilisation

### Mode Fichier
```bash
python error_analyzer.py mon_erreur.txt
```

### Mode Programmatique
```python
from error_analyzer import ErrorAnalyzerChatbot

analyzer = ErrorAnalyzerChatbot()
results = analyzer.analyze_error_report("""
Traceback (most recent call last):
  File "test.py", line 5, in <module>
    print(x)
NameError: name 'x' is not defined
""")

print(results[0]['explanation'])
print(results[0]['solutions'])
```

## 🎯 Fonctionnalités Principales

| Fonctionnalité | Commande |
|----------------|----------|
| Mode interactif | `python error_analyzer.py` |
| Analyser un fichier | `python error_analyzer.py fichier.txt` |
| Tests | `python test_error_analyzer.py` |
| Démonstration | `python demo.py` |
| Exemple d'usage | `python example_usage.py` |

## 📚 Documentation Complète

Pour plus de détails, consultez [ERROR_ANALYZER_README.md](ERROR_ANALYZER_README.md)

## 💡 Astuce

Le chatbot supporte:
- ✅ Python (NameError, SyntaxError, TypeError, etc.)
- ✅ JavaScript (ReferenceError, TypeError, etc.)
- ✅ Java (NullPointerException, etc.)
- ✅ Export JSON des analyses
- ✅ 13+ types d'erreurs dans la base de données
