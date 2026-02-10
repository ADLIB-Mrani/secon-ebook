# 🔄 N8N Workflow Guide

Guide pour configurer et utiliser les workflows N8N avec Secon E-book Generator.

## Table des Matières

- [Introduction](#introduction)
- [Installation](#installation)
- [Import du Workflow](#import-du-workflow)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Personnalisation](#personnalisation)
- [Exemples](#exemples)

## Introduction

N8N est une plateforme d'automatisation de workflows qui permet d'orchestrer la génération d'e-books de manière automatisée.

### Cas d'Usage

- Génération automatique périodique
- Agrégation de contenu depuis multiple sources
- Publication automatique vers cloud storage
- Notifications par email/Slack
- Intégration avec d'autres services

## Installation

### Via Docker (Recommandé)

N8N est déjà inclus dans le docker-compose :

```bash
docker-compose up -d n8n
```

Accéder à : http://localhost:5678

### Installation Standalone

```bash
npm install -g n8n
n8n start
```

## Import du Workflow

1. Accéder à N8N : http://localhost:5678
2. Se connecter :
   - Username: `admin`
   - Password: `changeme`
3. Cliquer sur "Import from File"
4. Sélectionner `/workflows/n8n-workflow.json`
5. Activer le workflow

## Configuration

### Webhook Configuration

Le workflow commence avec un webhook trigger :

```
URL: http://localhost:5678/webhook/ebook-trigger
Method: POST
```

### Payload Example

```json
{
  "title": "My Automated Ebook",
  "author": "N8N Automation",
  "format": "epub",
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ]
}
```

## Utilisation

### Déclencher via Webhook

```bash
curl -X POST http://localhost:5678/webhook/ebook-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech News Digest",
    "author": "Auto Generator",
    "format": "epub",
    "urls": [
      "https://news.ycombinator.com/best",
      "https://dev.to/top/week"
    ]
  }'
```

### Déclencher via Schedule

Modifier le workflow pour ajouter un nœud "Schedule":

1. Ajouter nœud "Schedule Trigger"
2. Configurer : Tous les jours à 9h00
3. Connecter aux autres nœuds

### Déclencher via API Backend

```python
import requests

webhook_url = "http://localhost:5678/webhook/ebook-trigger"
data = {
    "title": "Daily Digest",
    "author": "Bot",
    "format": "pdf",
    "urls": ["https://example.com"]
}

response = requests.post(webhook_url, json=data)
print(response.json())
```

## Workflow Détaillé

### Étapes du Workflow

1. **Webhook Trigger** - Reçoit la requête
2. **Create E-book** - Crée le projet via API
3. **Fetch URLs** - Récupère contenu des URLs
4. **Add Resources** - Ajoute contenu au projet
5. **Generate E-book** - Lance la génération
6. **Wait** - Attend la complétion
7. **Check Status** - Vérifie le statut
8. **If Complete** - Condition de succès
9. **Download E-book** - Télécharge le résultat
10. **Respond to Webhook** - Renvoie la réponse

## Personnalisation

### Ajouter Email Notification

```javascript
// Nœud Send Email
{
  "to": "user@example.com",
  "subject": "E-book Generated: {{ $json.title }}",
  "text": "Your e-book has been generated successfully!",
  "attachments": [{
    "filename": "ebook.epub",
    "data": "{{ $binary.data }}"
  }]
}
```

### Ajouter Slack Notification

```javascript
// Nœud Slack
{
  "channel": "#ebooks",
  "text": "📚 New e-book generated: {{ $json.title }}",
  "attachments": [{
    "title": "Download",
    "title_link": "{{ $json.download_url }}"
  }]
}
```

### Ajouter Upload vers Google Drive

```javascript
// Nœud Google Drive
{
  "operation": "upload",
  "name": "{{ $json.title }}.epub",
  "parents": ["folder_id"],
  "binaryData": true
}
```

## Exemples de Workflows

### 1. Daily News Aggregator

```json
{
  "schedule": "0 8 * * *",
  "sources": [
    "https://news.ycombinator.com/best",
    "https://reddit.com/r/programming/top"
  ],
  "format": "epub",
  "email_to": "reader@example.com"
}
```

### 2. Blog to E-book

```json
{
  "schedule": "0 0 * * 0",
  "source": "https://myblog.com/feed.xml",
  "filter": "published_last_week",
  "format": "pdf",
  "upload_to": "google_drive"
}
```

### 3. Research Paper Compiler

```json
{
  "trigger": "webhook",
  "sources": "arxiv_search",
  "keywords": ["machine learning", "AI"],
  "format": "pdf",
  "template": "academic"
}
```

## Monitoring

### Voir les Executions

1. Dans N8N, aller à "Executions"
2. Voir historique des runs
3. Debugger les erreurs

### Logs

```bash
# Docker logs
docker logs ebook-n8n -f

# Logs détaillés
docker-compose logs -f n8n
```

## Troubleshooting

### Webhook ne fonctionne pas

```bash
# Vérifier que N8N est accessible
curl http://localhost:5678/healthz

# Vérifier le webhook
curl -X POST http://localhost:5678/webhook/ebook-trigger
```

### Erreur de connexion au backend

Vérifier que backend est accessible depuis N8N :

```bash
# Dans container N8N
docker exec -it ebook-n8n sh
curl http://backend:8000/health
```

### Timeout

Augmenter timeout dans settings N8N :
- Workflow Settings > Execution Timeout: 3600s

## Sécurité

### Authentification Webhook

Ajouter authentification :

```javascript
// Nœud Function avant traitement
if ($json.headers.authorization !== 'Bearer YOUR_SECRET') {
  throw new Error('Unauthorized');
}
```

### HTTPS

Pour production, utiliser HTTPS:

```env
N8N_PROTOCOL=https
N8N_HOST=n8n.yourdomain.com
WEBHOOK_URL=https://n8n.yourdomain.com/
```

## Backup & Restore

### Export Workflows

1. Settings > Export Workflow
2. Sauvegarder le JSON

### Import Workflows

```bash
# Via CLI
docker exec -it ebook-n8n n8n import:workflow --input=/path/to/workflow.json
```

## Best Practices

1. **Error Handling** - Ajouter nœuds d'erreur
2. **Retry Logic** - Configurer retries
3. **Monitoring** - Setup alertes
4. **Version Control** - Versioner workflows
5. **Documentation** - Documenter chaque nœud

## Resources

- [N8N Documentation](https://docs.n8n.io/)
- [N8N Community](https://community.n8n.io/)
- [Workflow Examples](https://n8n.io/workflows)

## Support

Pour aide avec N8N :
- Documentation : https://docs.n8n.io/
- Community Forum : https://community.n8n.io/
- GitHub Issues : https://github.com/n8n-io/n8n/issues
