# 📖 User Guide - Secon E-book Generator

Guide complet d'utilisation pour créer des e-books professionnels.

## Table des Matières

- [Démarrage Rapide](#démarrage-rapide)
- [Créer votre Premier E-book](#créer-votre-premier-e-book)
- [Sources de Contenu](#sources-de-contenu)
- [Templates](#templates)
- [Génération](#génération)
- [Téléchargement](#téléchargement)
- [Astuces & Best Practices](#astuces--best-practices)

## Démarrage Rapide

### Accès à l'Application

1. Assurez-vous que Docker est en cours d'exécution
2. Démarrez l'application :
   ```bash
   docker-compose up -d
   ```
3. Ouvrez votre navigateur à : http://localhost:3000

### Interface Principale

L'interface se compose de :
- **Home** - Page d'accueil
- **Dashboard** - Vos projets e-books
- **Create** - Créer un nouveau e-book

## Créer votre Premier E-book

### Étape 1 : Informations de Base

1. Cliquez sur "Create New E-book"
2. Remplissez les informations :
   - **Titre*** : Le titre de votre e-book
   - **Auteur** : Votre nom (optionnel)
   - **Description** : Brève description
   - **Format** : EPUB, PDF, HTML ou MOBI
   - **Template** : Choisissez un style (optionnel)

3. Cliquez sur "Create E-book"

### Étape 2 : Ajouter du Contenu

Plusieurs options disponibles :

#### Upload de Fichiers

1. **Glissez-déposez** des fichiers dans la zone
2. Ou **cliquez** pour sélectionner
3. Formats supportés :
   - PDF (.pdf)
   - Word (.docx)
   - Texte (.txt)
   - Markdown (.md)
   - HTML (.html)
   - EPUB (.epub)

**Limites** :
- Taille max : 50 MB par fichier
- Maximum 10 fichiers

#### Ajouter une URL

1. Collez l'URL dans le champ
2. **JavaScript rendering** : Cochez si le site est dynamique
3. Cliquez sur "+"

**Exemples d'URLs** :
- Articles de blog
- Pages Wikipedia
- Documentation technique
- Articles de presse

#### Saisie Directe (Future)

Éditeur Markdown intégré pour écrire directement.

### Étape 3 : Générer

1. Vérifiez que tout le contenu est ajouté
2. Cliquez sur "Generate E-book"
3. Attendez la fin du traitement (barre de progression)

### Étape 4 : Télécharger

1. Retournez au Dashboard
2. Trouvez votre e-book (statut "completed")
3. Cliquez sur "Download"

## Sources de Contenu

### Upload de Fichiers

#### PDF
- Extraction de texte automatique
- Préservation de la structure
- Peut perdre le formatage complexe

#### DOCX (Word)
- Meilleure préservation du formatage
- Tables et images supportées
- Styles conservés

#### Markdown
- Format recommandé
- Conversion HTML parfaite
- Supporte code highlighting

#### HTML
- Scraping automatique
- Nettoyage du code
- Extraction du contenu principal

### Web Scraping

#### Mode Standard (BeautifulSoup)
**Avantages** :
- Rapide
- Faible utilisation ressources
- Parfait pour HTML statique

**Inconvénients** :
- Ne supporte pas JavaScript
- Peut manquer du contenu dynamique

**Quand l'utiliser** :
- Articles de blog
- Documentation statique
- Pages HTML simples

#### Mode JavaScript (Playwright)
**Avantages** :
- Supporte JavaScript
- Rendu complet de la page
- Contenu dynamique

**Inconvénients** :
- Plus lent
- Plus de ressources
- Peut être bloqué par certains sites

**Quand l'utiliser** :
- Sites avec contenu dynamique
- Applications React/Vue/Angular
- Sites avec lazy loading

### APIs Externes

#### Google Books
Rechercher et importer métadonnées :
```json
{
  "query": "Python programming",
  "max_results": 10
}
```

#### Archive.org
Contenu du domaine public :
```json
{
  "query": "classic literature",
  "media_type": "texts"
}
```

#### Unsplash
Images pour couvertures :
```json
{
  "query": "book cover",
  "count": 5
}
```

## Templates

### Templates Disponibles

#### 1. Novel
**Style** : Classique, élégant
**Police** : Georgia
**Usage** : Fiction, romans

**Caractéristiques** :
- Grandes marges
- Chapitres sur nouvelle page
- En-têtes avec titre
- Numéros de page centrés

#### 2. Technical Manual
**Style** : Professionnel, structuré
**Police** : Arial
**Usage** : Documentation technique

**Caractéristiques** :
- Table des matières
- Code highlighting
- Index automatique
- Références croisées

#### 3. Magazine
**Style** : Moderne, visuelles
**Police** : Helvetica
**Usage** : Articles, magazines

**Caractéristiques** :
- Colonnes multiples
- Images inline
- Sections colorées
- Design moderne

#### 4. Academic Paper
**Style** : Académique, formel
**Police** : Times New Roman
**Usage** : Papers, thèses

**Caractéristiques** :
- Double interligne
- Citations formatées
- Bibliographie automatique
- Numérotation académique

### Personnaliser un Template

1. Sélectionnez un template de base
2. (Future) Modifier les paramètres :
   - Polices
   - Couleurs
   - Marges
   - En-têtes/pieds de page

## Génération

### Processus de Génération

```
1. Collecte des ressources
2. Extraction du contenu
3. Nettoyage et formatage
4. Création de la structure
5. Application du template
6. Génération du fichier
7. Optimisation
8. Finalisation
```

### Temps de Génération

**Facteurs affectant la durée** :
- Nombre de ressources
- Taille du contenu
- Format choisi (EPUB < PDF < MOBI)
- Template utilisé

**Estimations** :
- E-book simple (< 10 pages) : 10-30 secondes
- E-book moyen (10-50 pages) : 30-60 secondes
- E-book long (> 50 pages) : 1-3 minutes

### Formats de Sortie

#### EPUB
**Avantages** :
- Standard e-reader
- Adaptatif (reflow)
- Interactif
- Taille fichier petite

**Usage** :
- Liseuses (Kindle, Kobo, etc.)
- Applications mobiles
- Distribution large

#### PDF
**Avantages** :
- Mise en page fixe
- Universel
- Print-ready
- Annotations

**Usage** :
- Impression
- Lecture ordinateur
- Archivage

#### HTML
**Avantages** :
- Interactif
- Responsive
- Facilement modifiable
- SEO-friendly

**Usage** :
- Publication web
- Documentation en ligne
- Prévisualisation

#### MOBI (nécessite Calibre)
**Avantages** :
- Format Kindle natif
- Optimisé Amazon

**Usage** :
- Kindle uniquement

## Téléchargement

### Depuis le Dashboard

1. Aller au Dashboard
2. Trouver l'e-book (statut "completed")
3. Cliquer "Download"
4. Le fichier se télécharge automatiquement

### Via API

```bash
curl -O http://localhost:8000/api/v1/ebook/1/download
```

### Partage

**Options** :
- Télécharger et partager le fichier
- (Future) Lien de partage public
- (Future) Envoi par email

## Astuces & Best Practices

### Qualité du Contenu

✅ **Bonnes Pratiques** :
- Utiliser du contenu bien formaté
- Préférer Markdown ou DOCX
- Vérifier les URLs avant ajout
- Organiser le contenu logiquement

❌ **À Éviter** :
- PDF scannés (sans OCR)
- Sites avec paywall
- Contenu protégé par droits d'auteur
- URLs cassées

### Optimisation Scraping

**Pour de Meilleurs Résultats** :
1. Tester l'URL dans un navigateur
2. Vérifier que le contenu est accessible
3. Utiliser mode JavaScript si nécessaire
4. Attendre le chargement complet

### Organisation

**Structure Recommandée** :
1. Introduction (chapitre 1)
2. Contenu principal (chapitres 2-N)
3. Conclusion (chapitre N+1)
4. Annexes (optionnel)

### Templates

**Choisir le Bon Template** :
- **Fiction** → Novel
- **Code/Tech** → Technical Manual
- **Articles** → Magazine
- **Recherche** → Academic Paper

### Performance

**Optimiser la Génération** :
- Limiter nombre de ressources
- Utiliser fichiers locaux quand possible
- Éviter scraping inutile
- Nettoyer contenu avant ajout

## Troubleshooting

### Erreur de Génération

**Solutions** :
1. Vérifier que le contenu est valide
2. Essayer un format différent
3. Réduire taille du contenu
4. Vérifier les logs

### Scraping Échoue

**Solutions** :
1. Essayer mode JavaScript
2. Vérifier que l'URL est accessible
3. Vérifier robots.txt du site
4. Utiliser une URL alternative

### Fichier Corrompu

**Solutions** :
1. Regénérer l'e-book
2. Essayer un format différent
3. Vérifier les ressources sources
4. Contacter le support

## Exemples

### Exemple 1 : Blog to E-book

1. Créer e-book "My Blog Posts"
2. Ajouter URLs des articles
3. Template: Magazine
4. Format: EPUB
5. Générer et télécharger

### Exemple 2 : Documentation Technique

1. Créer e-book "API Documentation"
2. Upload fichiers Markdown
3. Template: Technical Manual
4. Format: PDF
5. Générer

### Exemple 3 : Compilation d'Articles

1. Créer e-book "Best of Tech News"
2. Scraper 10 URLs
3. Template: Magazine
4. Format: EPUB
5. Générer

## Support

**Besoin d'aide ?**
- 📖 Consultez la [documentation](../README.md)
- 💬 Ouvrez une [issue GitHub](https://github.com/ADLIB-Mrani/secon-ebook/issues)
- 📧 Contactez le support

## Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [EPUB Specs](https://www.w3.org/publishing/epub3/)
- [Best Practices E-books](https://kdp.amazon.com/help)

---

**Bon e-booking! 📚**
