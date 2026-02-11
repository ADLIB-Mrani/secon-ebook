#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur d'Erreurs de Programmation avec Chatbot
Analyse les rapports d'erreurs et fournit des explications et corrections via un chatbot
"""

import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ErrorInfo:
    """Information sur une erreur de programmation"""
    error_type: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    code_snippet: Optional[str] = None
    language: Optional[str] = None


class ErrorParser:
    """Parse les rapports d'erreurs de différents langages"""
    
    def __init__(self):
        self.patterns = {
            'python': {
                'traceback': r'Traceback \(most recent call last\):',
                'error_line': r'File "([^"]+)", line (\d+)',
                'error_type': r'(\w+Error): (.+)',
                'syntax_error': r'SyntaxError: (.+)',
            },
            'javascript': {
                'error_line': r'at (.+):(\d+):(\d+)',
                'error_type': r'(\w+Error): (.+)',
            },
            'java': {
                'error_line': r'at (.+)\((.+):(\d+)\)',
                'error_type': r'(\w+Exception): (.+)',
            }
        }
    
    def detect_language(self, error_report: str) -> str:
        """Détecte le langage de programmation à partir du rapport d'erreur"""
        if 'Traceback' in error_report and 'Error:' in error_report:
            return 'python'
        elif 'Exception in thread' in error_report or '.java:' in error_report:
            return 'java'
        elif 'Error:' in error_report and ('at ' in error_report or '.js:' in error_report):
            return 'javascript'
        return 'unknown'
    
    def parse_error(self, error_report: str) -> List[ErrorInfo]:
        """Parse un rapport d'erreur et extrait les informations"""
        language = self.detect_language(error_report)
        errors = []
        
        if language == 'python':
            errors.extend(self._parse_python_error(error_report))
        elif language == 'javascript':
            errors.extend(self._parse_javascript_error(error_report))
        elif language == 'java':
            errors.extend(self._parse_java_error(error_report))
        else:
            # Essayer de parser comme erreur générique
            errors.append(ErrorInfo(
                error_type='UnknownError',
                message=error_report.strip(),
                language=language
            ))
        
        return errors
    
    def _parse_python_error(self, error_report: str) -> List[ErrorInfo]:
        """Parse les erreurs Python"""
        errors = []
        lines = error_report.split('\n')
        
        file_path = None
        line_number = None
        code_snippet = None
        
        for i, line in enumerate(lines):
            # Chercher le fichier et la ligne
            file_match = re.search(self.patterns['python']['error_line'], line)
            if file_match:
                file_path = file_match.group(1)
                line_number = int(file_match.group(2))
                # La ligne de code est souvent la suivante
                if i + 1 < len(lines):
                    code_snippet = lines[i + 1].strip()
            
            # Chercher le type d'erreur
            error_match = re.search(self.patterns['python']['error_type'], line)
            if error_match:
                errors.append(ErrorInfo(
                    error_type=error_match.group(1),
                    message=error_match.group(2),
                    file=file_path,
                    line=line_number,
                    code_snippet=code_snippet,
                    language='python'
                ))
        
        return errors if errors else [ErrorInfo(
            error_type='PythonError',
            message=error_report.strip(),
            language='python'
        )]
    
    def _parse_javascript_error(self, error_report: str) -> List[ErrorInfo]:
        """Parse les erreurs JavaScript"""
        errors = []
        lines = error_report.split('\n')
        
        for line in lines:
            error_match = re.search(self.patterns['javascript']['error_type'], line)
            if error_match:
                file_match = re.search(self.patterns['javascript']['error_line'], error_report)
                file_path = None
                line_number = None
                
                if file_match:
                    file_path = file_match.group(1)
                    line_number = int(file_match.group(2))
                
                errors.append(ErrorInfo(
                    error_type=error_match.group(1),
                    message=error_match.group(2),
                    file=file_path,
                    line=line_number,
                    language='javascript'
                ))
        
        return errors if errors else [ErrorInfo(
            error_type='JavaScriptError',
            message=error_report.strip(),
            language='javascript'
        )]
    
    def _parse_java_error(self, error_report: str) -> List[ErrorInfo]:
        """Parse les erreurs Java"""
        errors = []
        lines = error_report.split('\n')
        
        for line in lines:
            error_match = re.search(self.patterns['java']['error_type'], line)
            if error_match:
                file_match = re.search(self.patterns['java']['error_line'], error_report)
                file_path = None
                line_number = None
                
                if file_match:
                    file_path = file_match.group(2)
                    line_number = int(file_match.group(3))
                
                errors.append(ErrorInfo(
                    error_type=error_match.group(1),
                    message=error_match.group(2),
                    file=file_path,
                    line=line_number,
                    language='java'
                ))
        
        return errors if errors else [ErrorInfo(
            error_type='JavaException',
            message=error_report.strip(),
            language='java'
        )]


class ErrorChatbot:
    """Chatbot qui explique les erreurs et propose des corrections"""
    
    def __init__(self):
        self.error_database = self._load_error_database()
    
    def _load_error_database(self) -> Dict:
        """Charge la base de données d'explications d'erreurs"""
        return {
            'NameError': {
                'explanation': "Cette erreur se produit lorsque vous essayez d'utiliser une variable qui n'a pas été définie.",
                'causes': [
                    'Variable non déclarée',
                    'Faute de frappe dans le nom de la variable',
                    'Variable dans un scope différent'
                ],
                'solutions': [
                    'Vérifiez que la variable est bien définie avant utilisation',
                    'Vérifiez l\'orthographe du nom de la variable',
                    'Assurez-vous que la variable est dans le bon scope'
                ]
            },
            'SyntaxError': {
                'explanation': "Cette erreur indique une erreur de syntaxe dans votre code.",
                'causes': [
                    'Parenthèses, crochets ou accolades non fermés',
                    'Deux points manquants après if, for, while, def, class',
                    'Indentation incorrecte',
                    'Utilisation de mots-clés réservés comme noms de variables'
                ],
                'solutions': [
                    'Vérifiez que toutes les parenthèses sont bien fermées',
                    'Ajoutez les deux points manquants',
                    'Corrigez l\'indentation',
                    'Utilisez un nom de variable différent'
                ]
            },
            'TypeError': {
                'explanation': "Cette erreur se produit lorsqu'une opération est appliquée à un objet d'un type inapproprié.",
                'causes': [
                    'Opération entre types incompatibles',
                    'Nombre incorrect d\'arguments pour une fonction',
                    'Tentative de modification d\'un objet immuable'
                ],
                'solutions': [
                    'Convertissez les types si nécessaire (str(), int(), float())',
                    'Vérifiez le nombre d\'arguments passés à la fonction',
                    'Utilisez le bon type de données'
                ]
            },
            'ValueError': {
                'explanation': "Cette erreur se produit lorsqu'une fonction reçoit un argument du bon type mais avec une valeur inappropriée.",
                'causes': [
                    'Conversion impossible (ex: int("abc"))',
                    'Valeur hors limites',
                    'Format de données incorrect'
                ],
                'solutions': [
                    'Validez les données avant conversion',
                    'Utilisez try/except pour gérer les erreurs de conversion',
                    'Vérifiez le format des données d\'entrée'
                ]
            },
            'IndexError': {
                'explanation': "Cette erreur se produit lorsque vous essayez d'accéder à un index qui n'existe pas dans une liste.",
                'causes': [
                    'Index supérieur à la taille de la liste',
                    'Index négatif trop grand',
                    'Liste vide'
                ],
                'solutions': [
                    'Vérifiez la taille de la liste avant d\'accéder à un index',
                    'Utilisez len() pour connaître la taille',
                    'Vérifiez que la liste n\'est pas vide'
                ]
            },
            'KeyError': {
                'explanation': "Cette erreur se produit lorsque vous essayez d'accéder à une clé qui n'existe pas dans un dictionnaire.",
                'causes': [
                    'Clé inexistante dans le dictionnaire',
                    'Faute de frappe dans le nom de la clé'
                ],
                'solutions': [
                    'Utilisez .get() au lieu de [] pour un accès sécurisé',
                    'Vérifiez que la clé existe avec "in"',
                    'Vérifiez l\'orthographe de la clé'
                ]
            },
            'AttributeError': {
                'explanation': "Cette erreur se produit lorsque vous essayez d'accéder à un attribut ou une méthode qui n'existe pas.",
                'causes': [
                    'Attribut ou méthode inexistant',
                    'Faute de frappe',
                    'Objet de type None'
                ],
                'solutions': [
                    'Vérifiez la documentation de l\'objet',
                    'Utilisez dir() pour voir les attributs disponibles',
                    'Vérifiez que l\'objet n\'est pas None'
                ]
            },
            'ImportError': {
                'explanation': "Cette erreur se produit lorsque Python ne peut pas importer un module.",
                'causes': [
                    'Module non installé',
                    'Faute de frappe dans le nom du module',
                    'Module dans un chemin non accessible'
                ],
                'solutions': [
                    'Installez le module avec pip install',
                    'Vérifiez l\'orthographe du nom du module',
                    'Vérifiez le PYTHONPATH'
                ]
            },
            'ZeroDivisionError': {
                'explanation': "Cette erreur se produit lorsque vous essayez de diviser par zéro.",
                'causes': [
                    'Division par zéro explicite',
                    'Variable valant zéro utilisée comme diviseur'
                ],
                'solutions': [
                    'Vérifiez que le diviseur n\'est pas zéro avant la division',
                    'Utilisez try/except pour gérer cette erreur',
                    'Ajoutez une condition if pour éviter la division par zéro'
                ]
            },
            'FileNotFoundError': {
                'explanation': "Cette erreur se produit lorsque vous essayez d'ouvrir un fichier qui n'existe pas.",
                'causes': [
                    'Chemin de fichier incorrect',
                    'Fichier supprimé ou déplacé',
                    'Permissions insuffisantes'
                ],
                'solutions': [
                    'Vérifiez le chemin du fichier',
                    'Utilisez os.path.exists() pour vérifier l\'existence',
                    'Vérifiez les permissions du fichier'
                ]
            },
            'IndentationError': {
                'explanation': "Cette erreur se produit lorsque l'indentation de votre code est incorrecte.",
                'causes': [
                    'Mélange d\'espaces et de tabulations',
                    'Indentation incohérente',
                    'Indentation manquante après if, for, while, def, class'
                ],
                'solutions': [
                    'Utilisez uniquement des espaces (4 espaces recommandés)',
                    'Configurez votre éditeur pour convertir les tabs en espaces',
                    'Vérifiez l\'indentation de tout le bloc'
                ]
            },
            'ReferenceError': {
                'explanation': "Erreur JavaScript lorsqu'une variable n'est pas définie.",
                'causes': [
                    'Variable non déclarée',
                    'Variable hors du scope'
                ],
                'solutions': [
                    'Déclarez la variable avec let, const ou var',
                    'Vérifiez le scope de la variable'
                ]
            },
            'NullPointerException': {
                'explanation': "Erreur Java lorsqu'on tente d'utiliser une référence null.",
                'causes': [
                    'Objet non initialisé',
                    'Méthode retournant null'
                ],
                'solutions': [
                    'Vérifiez que l\'objet n\'est pas null avant utilisation',
                    'Initialisez les objets correctement',
                    'Utilisez Optional en Java 8+'
                ]
            }
        }
    
    def explain_error(self, error_info: ErrorInfo) -> Dict:
        """Explique une erreur et propose des corrections"""
        error_type = error_info.error_type
        
        # Chercher l'explication dans la base de données
        explanation = self.error_database.get(error_type, {
            'explanation': f"Erreur de type {error_type}.",
            'causes': ['Cause non identifiée - consultez la documentation'],
            'solutions': ['Vérifiez le message d\'erreur complet', 'Consultez la documentation du langage']
        })
        
        response = {
            'error_type': error_type,
            'message': error_info.message,
            'file': error_info.file,
            'line': error_info.line,
            'code_snippet': error_info.code_snippet,
            'language': error_info.language,
            'explanation': explanation['explanation'],
            'causes_possibles': explanation['causes'],
            'solutions': explanation['solutions'],
            'timestamp': datetime.now().isoformat()
        }
        
        return response
    
    def chat(self, user_message: str) -> str:
        """Interface de chat pour poser des questions sur les erreurs"""
        # Logique simple de chatbot
        user_message_lower = user_message.lower()
        
        if 'bonjour' in user_message_lower or 'salut' in user_message_lower:
            return "Bonjour! Je suis votre assistant pour analyser les erreurs de programmation. Envoyez-moi un rapport d'erreur et je vous aiderai à le comprendre et le corriger."
        
        elif 'aide' in user_message_lower or 'help' in user_message_lower:
            return """Je peux vous aider avec les erreurs de programmation!
            
Fonctionnalités:
1. Analyser les rapports d'erreurs Python, JavaScript et Java
2. Expliquer les causes des erreurs
3. Proposer des solutions
4. Répondre à vos questions sur les erreurs

Pour commencer, collez simplement votre rapport d'erreur."""
        
        elif 'merci' in user_message_lower:
            return "De rien! N'hésitez pas si vous avez d'autres erreurs à analyser."
        
        else:
            return "Je n'ai pas bien compris votre question. Pouvez-vous reformuler ou coller un rapport d'erreur à analyser?"


class ErrorAnalyzerChatbot:
    """Classe principale qui combine le parser et le chatbot"""
    
    def __init__(self):
        self.parser = ErrorParser()
        self.chatbot = ErrorChatbot()
        self.conversation_history = []
    
    def analyze_error_report(self, error_report: str) -> List[Dict]:
        """Analyse un rapport d'erreur complet"""
        errors = self.parser.parse_error(error_report)
        results = []
        
        for error in errors:
            explanation = self.chatbot.explain_error(error)
            results.append(explanation)
        
        return results
    
    def interactive_chat(self):
        """Mode interactif du chatbot"""
        print("=" * 70)
        print("🤖 Chatbot d'Analyse d'Erreurs de Programmation")
        print("=" * 70)
        print(self.chatbot.chat("bonjour"))
        print("\nTapez 'quit' ou 'exit' pour quitter.\n")
        
        while True:
            user_input = input("\n👤 Vous: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'quitter']:
                print("\n🤖 Assistant: Au revoir! Bon codage!")
                break
            
            if not user_input:
                continue
            
            # Vérifier si c'est un rapport d'erreur
            if any(keyword in user_input for keyword in ['Error', 'Exception', 'Traceback', 'at ']):
                print("\n🔍 Analyse du rapport d'erreur en cours...\n")
                results = self.analyze_error_report(user_input)
                
                for i, result in enumerate(results, 1):
                    print(f"\n{'=' * 70}")
                    print(f"📋 Erreur #{i}: {result['error_type']}")
                    print(f"{'=' * 70}")
                    
                    if result['file']:
                        print(f"📁 Fichier: {result['file']}")
                    if result['line']:
                        print(f"📍 Ligne: {result['line']}")
                    if result['code_snippet']:
                        print(f"💻 Code: {result['code_snippet']}")
                    
                    print(f"\n💬 Message: {result['message']}")
                    print(f"\n📖 Explication:")
                    print(f"   {result['explanation']}")
                    
                    print(f"\n🔍 Causes possibles:")
                    for cause in result['causes_possibles']:
                        print(f"   • {cause}")
                    
                    print(f"\n✅ Solutions proposées:")
                    for solution in result['solutions']:
                        print(f"   • {solution}")
            else:
                # Réponse du chatbot
                response = self.chatbot.chat(user_input)
                print(f"\n🤖 Assistant: {response}")
    
    def analyze_from_file(self, file_path: str) -> List[Dict]:
        """Analyse un rapport d'erreur depuis un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                error_report = f.read()
            return self.analyze_error_report(error_report)
        except FileNotFoundError:
            print(f"❌ Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
            return []
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier: {e}")
            return []
    
    def export_analysis(self, results: List[Dict], output_file: str):
        """Exporte l'analyse au format JSON"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ Analyse exportée dans '{output_file}'")
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")


def main():
    """Fonction principale"""
    import sys
    
    analyzer = ErrorAnalyzerChatbot()
    
    # Si un fichier est passé en argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"📂 Analyse du fichier: {file_path}\n")
        results = analyzer.analyze_from_file(file_path)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{'=' * 70}")
                print(f"📋 Erreur #{i}: {result['error_type']}")
                print(f"{'=' * 70}")
                
                if result['file']:
                    print(f"📁 Fichier: {result['file']}")
                if result['line']:
                    print(f"📍 Ligne: {result['line']}")
                
                print(f"\n💬 Message: {result['message']}")
                print(f"\n📖 Explication:")
                print(f"   {result['explanation']}")
                
                print(f"\n✅ Solutions proposées:")
                for solution in result['solutions']:
                    print(f"   • {solution}")
            
            # Option d'export
            export = input("\n💾 Voulez-vous exporter l'analyse en JSON? (o/n): ").strip().lower()
            if export == 'o':
                output_file = input("📝 Nom du fichier de sortie (par défaut: analysis.json): ").strip()
                if not output_file:
                    output_file = "analysis.json"
                analyzer.export_analysis(results, output_file)
    else:
        # Mode interactif
        analyzer.interactive_chat()


if __name__ == "__main__":
    main()
