# 🚀 Quick Start Guide

Get Secon E-book Generator up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- 2GB free disk space
- Internet connection

## 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/ADLIB-Mrani/secon-ebook.git
cd secon-ebook

# Copy environment file
cp .env.example .env

# (Optional) Edit .env to add API keys
nano .env
```

## 2. Start the Application

```bash
# Start all services
docker-compose up -d

# Check services are running
docker-compose ps
```

Expected output:
```
NAME                STATUS              PORTS
ebook-backend       Up                  0.0.0.0:8000->8000/tcp
ebook-frontend      Up                  0.0.0.0:3000->3000/tcp
ebook-db            Up (healthy)        0.0.0.0:5432->5432/tcp
ebook-redis         Up (healthy)        0.0.0.0:6379->6379/tcp
ebook-celery        Up
ebook-n8n           Up                  0.0.0.0:5678->5678/tcp
```

## 3. Access the Application

Open your browser and visit:

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **N8N Workflows**: http://localhost:5678

## 4. Create Your First E-book

### Via Web Interface

1. Go to http://localhost:3000
2. Click "Create New E-book"
3. Fill in:
   - Title: "My First E-book"
   - Author: Your name
   - Format: EPUB
4. Click "Create E-book"
5. Upload a file or add a URL
6. Click "Generate E-book"
7. Wait for completion
8. Download your e-book!

### Via API (Command Line)

```bash
# 1. Create e-book
EBOOK_ID=$(curl -s -X POST http://localhost:8000/api/v1/ebook/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First E-book",
    "author": "Me",
    "format": "epub"
  }' | jq -r '.id')

echo "Created e-book ID: $EBOOK_ID"

# 2. Add content from URL
curl -X POST http://localhost:8000/api/v1/ebook/$EBOOK_ID/resources \
  -H "Content-Type: application/json" \
  -d '{
    "type": "url",
    "source": "https://en.wikipedia.org/wiki/Book",
    "title": "Wikipedia: Book"
  }'

# 3. Generate
curl -X POST http://localhost:8000/api/v1/ebook/$EBOOK_ID/generate \
  -H "Content-Type: application/json" \
  -d '{"auto_extract": true}'

# 4. Wait a bit
sleep 30

# 5. Check status
curl http://localhost:8000/api/v1/ebook/$EBOOK_ID/status

# 6. Download
curl http://localhost:8000/api/v1/ebook/$EBOOK_ID/download -o my-ebook.epub
```

## 5. Try the Example

```bash
# Use the provided example
cd examples

# Create e-book from sample
curl -X POST http://localhost:8000/api/v1/ebook/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Example E-book",
    "author": "Secon",
    "format": "epub"
  }'

# Upload sample content
curl -X POST http://localhost:8000/api/v1/ebook/1/upload \
  -F "file=@sample-content.md"

# Generate
curl -X POST http://localhost:8000/api/v1/ebook/1/generate \
  -H "Content-Type: application/json" \
  -d '{"auto_extract": true}'
```

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery
docker-compose logs -f frontend
```

### Restart Services

```bash
# All services
docker-compose restart

# Specific service
docker-compose restart backend
```

### Stop Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

### Access Database

```bash
# Connect to PostgreSQL
docker exec -it ebook-db psql -U user -d ebook

# List tables
\dt

# Exit
\q
```

### Access Redis

```bash
# Connect to Redis
docker exec -it ebook-redis redis-cli

# Check keys
KEYS *

# Exit
exit
```

## Troubleshooting

### Port Already in Use

If port 3000, 8000, or 5432 is already in use:

```bash
# Edit docker-compose.yml
# Change port mapping, e.g., "3001:3000" instead of "3000:3000"
```

### Services Not Starting

```bash
# Check logs
docker-compose logs

# Restart
docker-compose down
docker-compose up -d
```

### Frontend Can't Connect to Backend

```bash
# Check frontend environment
docker exec ebook-frontend env | grep VITE

# Should show:
# VITE_API_URL=http://localhost:8000
```

### Celery Worker Not Processing

```bash
# Check Celery logs
docker-compose logs celery

# Restart Celery
docker-compose restart celery
```

## Next Steps

1. **Add API Keys** - Get free API keys and add to `.env` (see [API_KEYS.md](docs/API_KEYS.md))
2. **Read Documentation** - Check out [User Guide](docs/USER_GUIDE.md)
3. **Try Templates** - Experiment with different templates
4. **Explore API** - Visit http://localhost:8000/docs
5. **Setup N8N** - Create automated workflows

## Getting Help

- 📖 **Documentation**: [README.md](README.md)
- 💬 **Issues**: [GitHub Issues](https://github.com/ADLIB-Mrani/secon-ebook/issues)
- 📚 **User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- 🏗️ **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Development Setup

If you want to develop locally without Docker:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## API Keys (Optional)

For full functionality, get free API keys:

1. **Hugging Face** - https://huggingface.co/settings/tokens
2. **Unsplash** - https://unsplash.com/developers
3. **Google Books** - https://console.cloud.google.com/

Add them to `.env`:

```env
HUGGINGFACE_API_KEY=hf_xxxxx
UNSPLASH_ACCESS_KEY=xxxxx
GOOGLE_BOOKS_API_KEY=xxxxx
```

---

**Congratulations! 🎉**

You now have a fully functional e-book generation system!

Start creating amazing e-books! 📚
