# 🔑 API Keys Guide

Guide pour obtenir les clés API gratuites nécessaires au fonctionnement de Secon E-book.

## APIs Gratuites Supportées

Toutes ces APIs offrent un tier gratuit généreux, parfait pour commencer.

## 1. Hugging Face 🤗

**Usage:** NLP, résumés automatiques, traduction

### Obtenir la clé

1. Créer un compte sur [huggingface.co](https://huggingface.co/)
2. Aller sur [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Cliquer "New token"
4. Nom: `secon-ebook`
5. Role: `Read`
6. Copier le token

### Configuration

```env
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
```

### Limites Gratuites
- 30,000 requêtes/mois
- Rate limit: 60 requêtes/minute

### Modèles Utilisés
- `facebook/bart-large-cnn` - Résumés
- `Helsinki-NLP/opus-mt-*` - Traduction

## 2. Unsplash 📸

**Usage:** Images gratuites haute qualité pour couvertures

### Obtenir la clé

1. Créer compte sur [unsplash.com/developers](https://unsplash.com/developers)
2. Créer nouvelle application
3. Remplir le formulaire :
   - Application name: `Secon Ebook Generator`
   - Description: `E-book generation tool`
4. Accepter les termes
5. Copier l'Access Key

### Configuration

```env
UNSPLASH_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
```

### Limites Gratuites
- 50 requêtes/heure
- 5,000 requêtes/mois démonstration

### Guidelines
- Attribution requise pour usage commercial
- Télécharger depuis l'endpoint `/download`

## 3. Google Books API 📚

**Usage:** Métadonnées de livres, suggestions

### Obtenir la clé

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer nouveau projet ou sélectionner existant
3. Activer "Books API" :
   - Menu > APIs & Services > Library
   - Rechercher "Books API"
   - Cliquer "Enable"
4. Créer identifiants :
   - APIs & Services > Credentials
   - Create Credentials > API Key
   - Copier la clé

### Configuration

```env
GOOGLE_BOOKS_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Limites Gratuites
- 1,000 requêtes/jour
- Augmentable en activant facturation

### Sécurité
- Restreindre la clé à Books API uniquement
- Ajouter restrictions d'application si nécessaire

## 4. RapidAPI 🚀

**Usage:** Accès à multiples APIs (Wikipedia, Dictionary, etc.)

### Obtenir la clé

1. S'inscrire sur [rapidapi.com](https://rapidapi.com/)
2. Aller sur profile > [Keys](https://rapidapi.com/developer/dashboard)
3. Copier "X-RapidAPI-Key"

### Configuration

```env
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxx
```

### APIs Utiles (Gratuites)

#### Wikipedia API
- URL: `https://rapidapi.com/wovenware/api/wikipedia`
- Free: 500 requêtes/mois

#### Dictionary API
- URL: `https://rapidapi.com/twinword/api/twinword-dictionary`
- Free: 500 requêtes/mois

#### Text Analysis
- URL: `https://rapidapi.com/twinword/api/text-analysis`
- Free: 500 requêtes/mois

## 5. OpenLibrary 📖

**Usage:** Informations bibliographiques

### Aucune clé requise! 🎉

OpenLibrary est entièrement gratuit et ne nécessite pas d'authentification.

### Endpoints
```
https://openlibrary.org/search.json?q={query}
https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}
```

### Limites
- Fair use: ~100 requêtes/minute
- Pas de limite stricte pour usage raisonnable

## 6. Archive.org 🏛️

**Usage:** Contenu libre de droits, livres du domaine public

### Aucune clé requise! 🎉

Archive.org API est gratuite et ouverte.

### Endpoints
```
https://archive.org/advancedsearch.php?q={query}&output=json
https://archive.org/metadata/{identifier}
```

### Limites
- Pas de limite stricte
- Usage respectueux recommandé

## 7. OpenAI (Optionnel) 🧠

**Usage:** Enrichissement avancé de contenu

### Obtenir la clé

1. Créer compte sur [platform.openai.com](https://platform.openai.com/)
2. Ajouter méthode de paiement
3. Aller sur [API Keys](https://platform.openai.com/api-keys)
4. Créer nouvelle clé

### Configuration

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### Coûts
- Pay-as-you-go
- GPT-3.5-turbo: ~$0.002/1K tokens
- Crédit gratuit de $5 pour nouveaux comptes

## Configuration Complète

Fichier `.env` avec toutes les clés :

```env
# APIs Gratuites (Recommandées)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
UNSPLASH_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
GOOGLE_BOOKS_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxx
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxx

# Optionnel (Payant)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

## Vérification des Clés

Script Python pour tester les clés :

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_huggingface():
    key = os.getenv('HUGGINGFACE_API_KEY')
    if not key:
        return "❌ Clé non configurée"
    
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.get(
        "https://huggingface.co/api/whoami-v2",
        headers=headers
    )
    return "✅ OK" if response.status_code == 200 else "❌ Invalide"

def test_unsplash():
    key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not key:
        return "❌ Clé non configurée"
    
    response = requests.get(
        f"https://api.unsplash.com/photos?client_id={key}&per_page=1"
    )
    return "✅ OK" if response.status_code == 200 else "❌ Invalide"

def test_google_books():
    key = os.getenv('GOOGLE_BOOKS_API_KEY')
    if not key:
        return "❌ Clé non configurée"
    
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q=python&key={key}"
    )
    return "✅ OK" if response.status_code == 200 else "❌ Invalide"

print("Test des clés API:")
print(f"Hugging Face: {test_huggingface()}")
print(f"Unsplash: {test_unsplash()}")
print(f"Google Books: {test_google_books()}")
```

## Sécurité

### ⚠️ Importantes Pratiques

1. **Ne jamais commiter les clés dans Git**
   ```bash
   # Vérifier .gitignore
   echo ".env" >> .gitignore
   ```

2. **Utiliser des variables d'environnement**
   ```bash
   # Linux/macOS
   export HUGGINGFACE_API_KEY=xxx
   
   # Windows
   set HUGGINGFACE_API_KEY=xxx
   ```

3. **Rotation régulière des clés**
   - Changer les clés tous les 3-6 mois
   - Révoquer immédiatement si exposées

4. **Restrictions par clé**
   - Google Books: Restreindre aux IPs serveur
   - Unsplash: Configurer domaine référent

## Monitoring Usage

### Hugging Face
Dashboard: https://huggingface.co/settings/billing

### Unsplash
Dashboard: https://unsplash.com/oauth/applications

### Google Books
Console: https://console.cloud.google.com/apis/dashboard

### RapidAPI
Dashboard: https://rapidapi.com/developer/dashboard

## Troubleshooting

### Erreur 401 Unauthorized
- Vérifier que la clé est correcte
- Vérifier le format (Bearer, API key, etc.)
- Vérifier que la clé n'est pas expirée

### Erreur 429 Too Many Requests
- Vous avez dépassé la limite
- Attendre ou upgrader le plan
- Implémenter du rate limiting

### Erreur 403 Forbidden
- API non activée (Google)
- Restrictions d'usage non respectées
- Vérifier les conditions d'utilisation

## Support

Pour aide :
- [Hugging Face Docs](https://huggingface.co/docs)
- [Unsplash API Docs](https://unsplash.com/documentation)
- [Google Books API Docs](https://developers.google.com/books)
- [RapidAPI Docs](https://docs.rapidapi.com/)

## Alternatives

Si une API ne fonctionne pas, alternatives:

### Alternative à Hugging Face
- OpenAI API (payant mais powerful)
- Cohere API (free tier disponible)

### Alternative à Unsplash
- Pexels API (gratuit)
- Pixabay API (gratuit)

### Alternative à Google Books
- OpenLibrary (gratuit, no key)
- GoodReads API (deprecated mais encore fonctionnel)
