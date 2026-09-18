# 🤖 Analyseur d'Erreurs de Programmation avec Chatbot

Un outil Python intelligent qui analyse les rapports d'erreurs de programmation et fournit des explications détaillées ainsi que des solutions via une interface chatbot interactive.

## 📋 Fonctionnalités

- ✅ **Analyse automatique** des rapports d'erreurs Python, JavaScript et Java
- 🔍 **Détection du langage** automatique
- 💬 **Interface chatbot** interactive pour poser des questions
- 📖 **Explications détaillées** des erreurs avec causes et solutions
- 📁 **Support de fichiers** - analysez des rapports d'erreurs depuis des fichiers
- 💾 **Export JSON** des analyses pour archivage ou traitement ultérieur
- 🎯 **Base de données** complète d'erreurs courantes

## 🚀 Installation

Aucune dépendance externe requise! Le script utilise uniquement la bibliothèque standard Python.

```bash
# Cloner le dépôt
git clone https://github.com/ADLIB-Mrani/secon-ebook.git
cd secon-ebook

# Le script est prêt à l'emploi
python error_analyzer.py
```

## 💡 Utilisation

### Mode Interactif

Lancez le chatbot en mode interactif:

```bash
python error_analyzer.py
```

Vous pouvez ensuite:
- Coller directement un rapport d'erreur pour l'analyser
- Poser des questions sur les erreurs
- Demander de l'aide avec "aide" ou "help"

### Analyse d'un Fichier

Analysez un rapport d'erreur depuis un fichier:

```bash
python error_analyzer.py examples/error_python_1.txt
```

### Exemples d'Utilisation

#### Exemple 1: Analyser une erreur Python

```bash
$ python error_analyzer.py examples/error_python_1.txt

📂 Analyse du fichier: examples/error_python_1.txt

======================================================================
📋 Erreur #1: ZeroDivisionError
======================================================================
📁 Fichier: test_script.py
📍 Ligne: 8

💬 Message: division by zero

📖 Explication:
   Cette erreur se produit lorsque vous essayez de diviser par zéro.

✅ Solutions proposées:
   • Vérifiez que le diviseur n'est pas zéro avant la division
   • Utilisez try/except pour gérer cette erreur
   • Ajoutez une condition if pour éviter la division par zéro
```

#### Exemple 2: Mode Interactif

```
$ python error_analyzer.py

======================================================================
🤖 Chatbot d'Analyse d'Erreurs de Programmation
======================================================================
Bonjour! Je suis votre assistant pour analyser les erreurs de programmation.

Tapez 'quit' ou 'exit' pour quitter.

👤 Vous: Traceback (most recent call last):
  File "test.py", line 5, in <module>
    print(user_name)
NameError: name 'user_name' is not defined

🔍 Analyse du rapport d'erreur en cours...

======================================================================
📋 Erreur #1: NameError
======================================================================
📁 Fichier: test.py
📍 Ligne: 5
💻 Code: print(user_name)

💬 Message: name 'user_name' is not defined

📖 Explication:
   Cette erreur se produit lorsque vous essayez d'utiliser une variable qui n'a pas été définie.

🔍 Causes possibles:
   • Variable non déclarée
   • Faute de frappe dans le nom de la variable
   • Variable dans un scope différent

✅ Solutions proposées:
   • Vérifiez que la variable est bien définie avant utilisation
   • Vérifiez l'orthographe du nom de la variable
   • Assurez-vous que la variable est dans le bon scope
```

## 📚 Types d'Erreurs Supportées

### Python
- NameError
- SyntaxError
- TypeError
- ValueError
- IndexError
- KeyError
- AttributeError
- ImportError
- ZeroDivisionError
- FileNotFoundError
- IndentationError

### JavaScript
- ReferenceError
- TypeError
- SyntaxError
- Et autres erreurs courantes

### Java
- NullPointerException
- ArrayIndexOutOfBoundsException
- Et autres exceptions courantes

## 🔧 Utilisation Programmatique

Vous pouvez également utiliser l'analyseur dans vos propres scripts:

```python
from error_analyzer import ErrorAnalyzerChatbot

# Créer une instance de l'analyseur
analyzer = ErrorAnalyzerChatbot()

# Analyser un rapport d'erreur
error_report = """
Traceback (most recent call last):
  File "test.py", line 5
    print(x
SyntaxError: unexpected EOF while parsing
"""

results = analyzer.analyze_error_report(error_report)

# Afficher les résultats
for result in results:
    print(f"Type: {result['error_type']}")
    print(f"Explication: {result['explanation']}")
    print(f"Solutions: {result['solutions']}")

# Exporter en JSON
analyzer.export_analysis(results, "analysis.json")
```

## 📁 Structure du Projet

```
secon-ebook/
├── error_analyzer.py          # Script principal
├── examples/                  # Exemples de rapports d'erreurs
│   ├── error_python_1.txt    # ZeroDivisionError
│   ├── error_python_2.txt    # NameError
│   ├── error_python_3.txt    # ValueError
│   └── error_python_4.txt    # IndexError
├── ERROR_ANALYZER_README.md  # Ce fichier
└── README.md                 # README principal du projet
```

## 🎯 Cas d'Usage

1. **Apprentissage**: Idéal pour les débutants qui veulent comprendre leurs erreurs
2. **Débogage**: Aide au diagnostic rapide des problèmes
3. **Documentation**: Génération de rapports d'erreurs documentés
4. **Formation**: Outil pédagogique pour enseigner le débogage
5. **Analyse de logs**: Traitement en batch de fichiers de logs d'erreurs

## 🔮 Fonctionnalités Futures

- [ ] Support de plus de langages (C++, C#, Ruby, etc.)
- [ ] Intégration avec des LLMs pour des explications plus contextuelles
- [ ] Interface web avec Flask/FastAPI
- [ ] Génération de code corrigé automatiquement
- [ ] Historique des erreurs analysées
- [ ] Statistiques sur les erreurs les plus fréquentes
- [ ] Support multi-langue (anglais, espagnol, etc.)

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Ajouter des explications pour de nouveaux types d'erreurs
- Améliorer la documentation

## 📄 Licence

MIT License - voir le fichier LICENSE pour plus de détails

## 👨‍💻 Auteur

Développé avec ❤️ pour aider les développeurs à mieux comprendre et corriger leurs erreurs.

---

💡 **Astuce**: Pour de meilleurs résultats, copiez le rapport d'erreur complet incluant le traceback!
