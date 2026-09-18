# 📚 Secon E-book - Générateur Automatique d'E-books

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

Système complet de génération automatique d'e-books à partir de multiples sources (URLs, fichiers, APIs) avec interface web moderne.

[Démo](#demo) • [Installation](#installation) • [Documentation](#documentation) • [Fonctionnalités](#fonctionnalités)

</div>

## 🤖 Analyseur d'Erreurs de Programmation

Un outil Python intelligent inclus dans ce projet qui analyse les rapports d'erreurs de programmation et fournit des explications détaillées ainsi que des solutions via une interface chatbot interactive.

### Utilisation Rapide

```bash
# Mode interactif
python error_analyzer.py

# Analyser un fichier d'erreur
python error_analyzer.py examples/error_python_1.txt

# Exécuter les tests
python test_error_analyzer.py
```

Pour plus de détails, consultez [ERROR_ANALYZER_README.md](ERROR_ANALYZER_README.md).

## ✨ Fonctionnalités

### 🎯 Principales Capacités

- **Sources Multiples**
  - 📤 Upload de fichiers (PDF, DOCX, TXT, MD, HTML, EPUB)
  - 🌐 Scraping web intelligent (BeautifulSoup + Playwright)
  - 🔌 Intégration d'APIs gratuites (Google Books, Archive.org, Unsplash)
  - ✍️ Saisie directe de texte avec éditeur Markdown

- **Génération Intelligente**
  - 📖 Export multi-formats (EPUB, PDF, HTML, MOBI)
  - 🎨 Templates personnalisables (Novel, Technical, Magazine, Academic)
  - 🤖 Enrichissement IA (résumés, traduction via Hugging Face)
  - 📑 Génération automatique de table des matières

- **Interface Moderne**
  - ⚡ React 18 + TypeScript
  - 🎨 Tailwind CSS + Shadcn/ui
  - 📱 Responsive design
  - 🔄 Drag & drop pour uploads
  - 📊 Dashboard avec suivi de projets

- **Infrastructure Robuste**
  - 🚀 FastAPI backend performant
  - 🔄 Celery + Redis pour tâches asynchrones
  - 🗄️ PostgreSQL/SQLite pour persistance
  - 🐳 Docker-compose pour déploiement facile
  - 🔧 N8N pour automatisation de workflows

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Node.js 18+ (pour développement local)
- Python 3.11+ (pour développement local)

### Installation Rapide avec Docker

```bash
# Cloner le repository
git clone https://github.com/ADLIB-Mrani/secon-ebook.git
cd secon-ebook

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer tous les services
docker-compose up -d

# Accéder à l'application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# N8N: http://localhost:5678
```

### Installation pour Développement

#### Backend

```bash
cd backend

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Configurer base de données
# Éditer .env pour DATABASE_URL

# Lancer serveur
uvicorn main:app --reload --port 8000

# Dans un autre terminal, lancer Celery worker
celery -A app.core.celery_app worker --loglevel=info
```

#### Frontend

```bash
cd frontend

# Installer dépendances
npm install

# Lancer serveur de développement
npm run dev

# Accéder à http://localhost:3000
```

## 📖 Utilisation

### Créer votre Premier E-book

1. **Accédez à l'interface** : http://localhost:3000
2. **Créez un nouveau projet** : Cliquez sur "Create New E-book"
3. **Remplissez les informations** :
   - Titre
   - Auteur
   - Format (EPUB, PDF, HTML, MOBI)
   - Template (optionnel)
4. **Ajoutez du contenu** :
   - Uploadez des fichiers
   - Ajoutez des URLs à scraper
   - Saisissez du texte directement
5. **Générez** : Cliquez sur "Generate E-book"
6. **Téléchargez** : Une fois terminé, téléchargez votre e-book

### Via API

```bash
# Créer un e-book
curl -X POST http://localhost:8000/api/v1/ebook/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mon Premier E-book",
    "author": "John Doe",
    "format": "epub"
  }'

# Ajouter une ressource
curl -X POST http://localhost:8000/api/v1/ebook/1/resources \
  -H "Content-Type: application/json" \
  -d '{
    "type": "url",
    "source": "https://example.com/article"
  }'

# Générer l'e-book
curl -X POST http://localhost:8000/api/v1/ebook/1/generate \
  -H "Content-Type: application/json" \
  -d '{"auto_extract": true}'

# Vérifier le statut
curl http://localhost:8000/api/v1/ebook/1/status

# Télécharger
curl http://localhost:8000/api/v1/ebook/1/download -o ebook.epub
```

## 🏗️ Architecture

```
secon-ebook/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/         # Routes API
│   │   ├── core/        # Configuration, DB, Celery
│   │   ├── models/      # Modèles SQLAlchemy
│   │   ├── services/    # Logique métier
│   │   └── utils/       # Utilitaires
│   └── main.py          # Point d'entrée
├── frontend/            # Application React
│   ├── src/
│   │   ├── components/  # Composants UI
│   │   ├── pages/       # Pages
│   │   ├── services/    # API client
│   │   └── store/       # State management
│   └── index.html
├── workflows/           # Workflows N8N
├── docs/               # Documentation
└── docker-compose.yml  # Configuration Docker
```

## 🔧 Configuration

### Variables d'Environnement

Voir [CONFIGURATION.md](./CONFIGURATION.md) pour la liste complète.

**Essentielles:**
```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/ebook

# Redis
REDIS_URL=redis://localhost:6379

# APIs (optionnelles mais recommandées)
HUGGINGFACE_API_KEY=your_key
UNSPLASH_ACCESS_KEY=your_key
GOOGLE_BOOKS_API_KEY=your_key
```

### Obtenir les Clés API

Voir [API_KEYS.md](./docs/API_KEYS.md) pour les instructions détaillées.

## 📚 Documentation

- [📖 Guide Utilisateur](./docs/USER_GUIDE.md) - Guide complet d'utilisation
- [🏗️ Architecture](./docs/ARCHITECTURE.md) - Documentation technique
- [⚙️ Configuration](./CONFIGURATION.md) - Guide de configuration
- [🔑 Clés API](./docs/API_KEYS.md) - Obtenir les clés API gratuites
- [🔄 Workflows N8N](./WORKFLOW.md) - Automatisation avec N8N
- [🗺️ Roadmap](./ROADMAP.md) - Fonctionnalités futures

## 🧪 Tests

### Backend
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web moderne
- **SQLAlchemy** - ORM
- **Celery** - Tâches asynchrones
- **Redis** - Cache et message broker
- **BeautifulSoup4** - Web scraping
- **Playwright** - Scraping JavaScript
- **ebooklib** - Génération EPUB
- **WeasyPrint** - Génération PDF

### Frontend
- **React 18** - Framework UI
- **TypeScript** - Typage statique
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client
- **React Router** - Routing

### Infrastructure
- **PostgreSQL** - Base de données
- **Redis** - Cache & queues
- **Docker** - Containerisation
- **N8N** - Workflow automation

## 🔌 Intégrations API

### APIs Gratuites Supportées

1. **Hugging Face** - NLP, résumés, traduction
2. **Unsplash** - Images de haute qualité
3. **Google Books** - Métadonnées de livres
4. **Archive.org** - Contenu libre de droits
5. **OpenLibrary** - Informations bibliographiques

Voir [API_KEYS.md](./docs/API_KEYS.md) pour plus de détails.

## 🚢 Déploiement

### Production avec Docker

```bash
# Build et démarrage
docker-compose -f docker-compose.yml up -d --build

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Arrêter et supprimer volumes
docker-compose down -v
```

### Variables d'Environnement Production

```env
DEBUG=False
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
DATABASE_URL=postgresql://user:password@db:5432/ebook
CORS_ORIGINS=https://votre-domaine.com
```

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **ADLIB-Mrani** - *Travail initial* - [GitHub](https://github.com/ADLIB-Mrani)

## 🙏 Remerciements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [N8N](https://n8n.io/)
- Toutes les APIs gratuites utilisées

## 📞 Support

- 💬 Issues: [GitHub Issues](https://github.com/ADLIB-Mrani/secon-ebook/issues)
- 📖 Documentation: [/docs](./docs/)

## 🔮 Roadmap

Voir [ROADMAP.md](./ROADMAP.md) pour les fonctionnalités planifiées :

- [ ] Support multi-langues
- [ ] Collaboration temps réel
- [ ] Intégration Git
- [ ] Export Amazon KDP
- [ ] OCR pour PDF scannés
- [ ] Génération audio book (TTS)
- [ ] Analytics
- [ ] Marketplace de templates

---

<div align="center">

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**

Fait avec ❤️ par ADLIB-Mrani

</div>