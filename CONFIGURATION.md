# ⚙️ Configuration Guide

Guide complet de configuration pour Secon E-book Generator.

## Table des Matières

- [Variables d'Environnement](#variables-denvironnement)
- [Configuration Base de Données](#configuration-base-de-données)
- [Configuration Redis](#configuration-redis)
- [APIs Externes](#apis-externes)
- [Configuration Celery](#configuration-celery)
- [Configuration Frontend](#configuration-frontend)
- [Configuration N8N](#configuration-n8n)
- [Configuration Production](#configuration-production)

## Variables d'Environnement

### Fichier .env Principal

Créez un fichier `.env` à la racine du projet :

```env
# ======================
# APPLICATION
# ======================
APP_NAME=Secon E-book Generator
APP_VERSION=1.0.0
DEBUG=False

# ======================
# DATABASE
# ======================
# SQLite (développement)
DATABASE_URL=sqlite:///./ebook.db

# PostgreSQL (production recommandée)
# DATABASE_URL=postgresql://user:password@localhost:5432/ebook

# ======================
# REDIS
# ======================
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# ======================
# SECURITY
# ======================
SECRET_KEY=your-very-long-random-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ======================
# CORS
# ======================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ======================
# FILE UPLOAD
# ======================
MAX_FILE_SIZE=52428800  # 50MB en bytes
ALLOWED_EXTENSIONS=pdf,docx,txt,md,html,epub
TEMP_DIR=/tmp/ebook_temp
OUTPUT_DIR=./generated_ebooks

# ======================
# EXTERNAL APIS
# ======================

# Hugging Face (NLP, Résumés, Traduction)
# Obtenir sur: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=

# Unsplash (Images gratuites)
# Obtenir sur: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY=

# Google Books (Métadonnées de livres)
# Obtenir sur: https://console.cloud.google.com/
GOOGLE_BOOKS_API_KEY=

# RapidAPI (APIs variées)
# Obtenir sur: https://rapidapi.com/
RAPIDAPI_KEY=

# OpenAI (optionnel, pour enrichissement avancé)
OPENAI_API_KEY=

# ======================
# N8N
# ======================
N8N_WEBHOOK_URL=http://localhost:5678/webhook
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=changeme

# ======================
# FRONTEND
# ======================
VITE_API_URL=http://localhost:8000
VITE_API_BASE_PATH=/api/v1
```

## Configuration Base de Données

### SQLite (Développement)

Simple et sans configuration :

```env
DATABASE_URL=sqlite:///./ebook.db
```

### PostgreSQL (Production)

#### Installation PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Démarrer le service
sudo service postgresql start  # Linux
brew services start postgresql  # macOS
```

#### Créer la base de données

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer utilisateur
CREATE USER ebook_user WITH PASSWORD 'secure_password';

-- Créer base de données
CREATE DATABASE ebook_db OWNER ebook_user;

-- Accorder privilèges
GRANT ALL PRIVILEGES ON DATABASE ebook_db TO ebook_user;
```

#### Configuration

```env
DATABASE_URL=postgresql://ebook_user:secure_password@localhost:5432/ebook_db
```

### Migrations (Alembic)

```bash
cd backend

# Initialiser Alembic
alembic init alembic

# Créer migration
alembic revision --autogenerate -m "Initial migration"

# Appliquer migrations
alembic upgrade head
```

## Configuration Redis

### Installation Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Démarrer Redis
redis-server

# Vérifier que Redis fonctionne
redis-cli ping
# Devrait retourner: PONG
```

### Configuration

```env
REDIS_URL=redis://localhost:6379
```

### Redis avec Authentification

```env
REDIS_URL=redis://:password@localhost:6379
```

### Redis distant

```env
REDIS_URL=redis://username:password@redis-host:6379/0
```

## APIs Externes

### Hugging Face

1. Créer un compte sur https://huggingface.co/
2. Aller sur https://huggingface.co/settings/tokens
3. Créer un nouveau token (Read)
4. Copier dans `.env`:

```env
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
```

### Unsplash

1. Créer compte sur https://unsplash.com/developers
2. Créer une nouvelle application
3. Copier l'Access Key

```env
UNSPLASH_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
```

### Google Books

1. Aller sur https://console.cloud.google.com/
2. Créer un projet
3. Activer "Books API"
4. Créer des identifiants (API Key)

```env
GOOGLE_BOOKS_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### RapidAPI

1. S'inscrire sur https://rapidapi.com/
2. Souscrire aux APIs gratuites souhaitées
3. Copier votre RapidAPI Key

```env
RAPIDAPI_KEY=xxxxxxxxxxxxxxxxxxxx
```

## Configuration Celery

### Variables Celery

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Lancer Celery Worker

```bash
# Développement
celery -A app.core.celery_app worker --loglevel=info

# Production avec autoreload
celery -A app.core.celery_app worker --loglevel=info --autoscale=10,3

# Avec Beat (tasks programmées)
celery -A app.core.celery_app worker --beat --loglevel=info
```

### Monitoring Celery (Flower)

```bash
# Installer Flower
pip install flower

# Lancer Flower
celery -A app.core.celery_app flower

# Accéder à http://localhost:5555
```

## Configuration Frontend

### Variables Vite

Créer `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
VITE_API_BASE_PATH=/api/v1
```

### Production

```env
VITE_API_URL=https://api.votredomaine.com
VITE_API_BASE_PATH=/api/v1
```

## Configuration N8N

### Accès N8N

```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=changeme
N8N_HOST=localhost
N8N_PORT=5678
```

### Importer Workflow

1. Accéder à http://localhost:5678
2. Se connecter (admin/changeme)
3. Cliquer "Import from File"
4. Sélectionner `workflows/n8n-workflow.json`

## Configuration Production

### Sécurité

```env
# Générer secret key sécurisée
SECRET_KEY=$(openssl rand -hex 32)

# Désactiver debug
DEBUG=False

# Configurer CORS
CORS_ORIGINS=https://votredomaine.com,https://www.votredomaine.com
```

### Performance

```env
# Augmenter timeout
REQUEST_TIMEOUT=300

# Pool de connexions DB
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Workers Celery
CELERY_WORKER_CONCURRENCY=4
```

### HTTPS

Pour production, configurez un reverse proxy (Nginx/Caddy):

```nginx
server {
    listen 443 ssl http2;
    server_name votredomaine.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Vérification Configuration

### Script de vérification

```bash
#!/bin/bash

echo "Vérification de la configuration..."

# Vérifier PostgreSQL
psql -U ebook_user -d ebook_db -c "SELECT 1" && echo "✓ PostgreSQL OK" || echo "✗ PostgreSQL Erreur"

# Vérifier Redis
redis-cli ping && echo "✓ Redis OK" || echo "✗ Redis Erreur"

# Vérifier backend
curl http://localhost:8000/health && echo "✓ Backend OK" || echo "✗ Backend Erreur"

# Vérifier frontend
curl http://localhost:3000 && echo "✓ Frontend OK" || echo "✗ Frontend Erreur"

echo "Vérification terminée!"
```

## Troubleshooting

### Erreur de connexion DB

```bash
# Vérifier que PostgreSQL écoute
sudo netstat -plnt | grep 5432

# Vérifier les logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Erreur Redis

```bash
# Redémarrer Redis
sudo service redis-server restart

# Vérifier statut
redis-cli ping
```

### Erreur Celery

```bash
# Vérifier les workers
celery -A app.core.celery_app inspect active

# Purger les tasks
celery -A app.core.celery_app purge
```

## Support

Pour plus d'aide :
- Voir [docs/USER_GUIDE.md](./docs/USER_GUIDE.md)
- Ouvrir une issue sur GitHub
