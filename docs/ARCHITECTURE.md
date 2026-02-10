# 🏗️ Architecture Documentation

Documentation technique détaillée de Secon E-book Generator.

## Vue d'Ensemble

Secon E-book est une application full-stack moderne construite avec une architecture microservices containerisée.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│   Frontend   │────▶│   Backend   │
│  (Browser)  │◀────│   (React)    │◀────│  (FastAPI)  │
└─────────────┘     └──────────────┘     └─────────────┘
                                                  │
                            ┌─────────────────────┼─────────────┐
                            │                     │             │
                       ┌────▼────┐          ┌────▼────┐   ┌────▼────┐
                       │PostgreSQL│          │  Redis  │   │  Celery │
                       │   (DB)   │          │ (Cache) │   │(Workers)│
                       └──────────┘          └─────────┘   └─────────┘
```

## Stack Technologique

### Frontend

- **React 18** - Library UI moderne
- **TypeScript** - Type safety
- **Vite** - Build tool rapide
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management léger
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Backend

- **FastAPI** - Framework web async
- **SQLAlchemy** - ORM
- **Pydantic** - Validation de données
- **Uvicorn** - ASGI server
- **Celery** - Task queue
- **Redis** - Message broker & cache
- **PostgreSQL** - Base de données principale

### Services

- **BeautifulSoup4** - HTML parsing
- **Playwright** - Browser automation
- **Newspaper3k** - Article extraction
- **ebooklib** - EPUB generation
- **WeasyPrint** - PDF generation
- **Markdown** - Markdown processing

## Architecture Détaillée

### Backend Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── ebook.py          # CRUD e-books
│   │       ├── resources.py      # Gestion ressources
│   │       └── templates.py      # Templates
│   ├── core/
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # DB connection
│   │   ├── security.py          # Auth & security
│   │   └── celery_app.py        # Celery setup
│   ├── models/
│   │   └── __init__.py          # SQLAlchemy models
│   ├── services/
│   │   ├── scraper.py           # Web scraping
│   │   ├── api_integrations.py  # External APIs
│   │   ├── ebook_generator.py   # E-book generation
│   │   ├── content_processor.py # Content processing
│   │   └── tasks.py             # Celery tasks
│   └── utils/
│       ├── file_handler.py      # File operations
│       └── validators.py        # Input validation
└── main.py                      # Entry point
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                  # Shared UI components
│   │   ├── upload/              # Upload components
│   │   ├── editor/              # Editor components
│   │   └── dashboard/           # Dashboard components
│   ├── pages/
│   │   ├── Home.tsx             # Landing page
│   │   ├── Dashboard.tsx        # Projects dashboard
│   │   └── CreateEbook.tsx      # Creation page
│   ├── services/
│   │   └── api.ts               # API client
│   ├── store/
│   │   └── ebookStore.ts        # Global state
│   └── App.tsx                  # Root component
```

## Data Flow

### E-book Creation Flow

```
1. User Input
   └─▶ Frontend (React)
       └─▶ API Request
           └─▶ Backend (FastAPI)
               └─▶ Database (Create record)
                   └─▶ Return E-book ID

2. Add Resources
   └─▶ Upload Files / Add URLs
       └─▶ Backend Processing
           ├─▶ File Storage
           ├─▶ URL Scraping (BeautifulSoup/Playwright)
           └─▶ Database (Store resources)

3. Generate E-book
   └─▶ Trigger Generation
       └─▶ Celery Task (Async)
           ├─▶ Fetch Resources
           ├─▶ Process Content
           ├─▶ Generate EPUB/PDF
           └─▶ Store Output

4. Download
   └─▶ Poll Status
       └─▶ Download File
```

## Database Schema

### Tables

#### ebooks
```sql
CREATE TABLE ebooks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    format VARCHAR(20),
    template_id INTEGER,
    cover_image_url VARCHAR(500),
    metadata JSONB,
    output_path VARCHAR(500),
    task_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

#### resources
```sql
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    ebook_id INTEGER REFERENCES ebooks(id),
    type VARCHAR(20),
    source TEXT,
    title VARCHAR(255),
    content TEXT,
    metadata JSONB,
    order INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### templates
```sql
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100),
    config JSONB,
    is_default INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### E-books

```
POST   /api/v1/ebook/create          - Create new e-book
GET    /api/v1/ebook/{id}            - Get e-book details
GET    /api/v1/ebook/                - List all e-books
POST   /api/v1/ebook/{id}/resources  - Add resource
POST   /api/v1/ebook/{id}/upload     - Upload file
POST   /api/v1/ebook/{id}/generate   - Generate e-book
GET    /api/v1/ebook/{id}/status     - Get generation status
GET    /api/v1/ebook/{id}/download   - Download e-book
DELETE /api/v1/ebook/{id}            - Delete e-book
```

### Templates

```
GET    /api/v1/templates/            - List templates
GET    /api/v1/templates/{id}        - Get template
POST   /api/v1/templates/            - Create template
```

### Resources

```
POST   /api/v1/resources/scrape           - Scrape URL
POST   /api/v1/resources/images/search    - Search images
POST   /api/v1/resources/books/search     - Search books
POST   /api/v1/resources/archive/search   - Search Archive.org
POST   /api/v1/resources/content/summarize - Summarize text
```

## Async Processing

### Celery Tasks

```python
@celery_app.task
def generate_ebook_task(ebook_id, title, author, chapters, format, output_path):
    """Async e-book generation"""
    # 1. Fetch resources
    # 2. Process content
    # 3. Generate file
    # 4. Update database
    return {'status': 'success', 'path': output_path}
```

### Task States

```
PENDING   → Task créée, en attente
PROCESSING → Task en cours
SUCCESS   → Task réussie
FAILURE   → Task échouée
```

## Security

### Authentication (Future)

- JWT tokens pour API
- Session-based pour web
- OAuth2 pour social login

### Input Validation

- Pydantic models pour validation
- Sanitization des inputs
- File type verification
- Size limits

### CORS

```python
CORSMiddleware(
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance

### Caching Strategy

- Redis pour sessions
- Redis pour task results
- Browser cache pour assets statiques

### Optimization

- Database indexing
- Connection pooling
- Async I/O
- Lazy loading

## Deployment

### Docker Architecture

```yaml
services:
  backend:    # FastAPI application
  frontend:   # React application
  db:         # PostgreSQL
  redis:      # Redis server
  celery:     # Celery workers
  n8n:        # Workflow automation
```

### Health Checks

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Monitoring

### Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics (Future)

- Prometheus pour metrics
- Grafana pour dashboards
- Sentry pour error tracking

## Testing Strategy

### Backend Tests

```bash
pytest tests/
pytest --cov=app tests/
```

### Frontend Tests

```bash
npm run test
npm run test:e2e
```

## Best Practices

1. **Code Quality**
   - Type hints (Python)
   - TypeScript strict mode
   - Linting (Black, ESLint)

2. **Security**
   - Input validation
   - SQL injection prevention
   - XSS protection

3. **Performance**
   - Async operations
   - Database indexing
   - Caching strategy

4. **Maintainability**
   - Clear code structure
   - Comprehensive docs
   - Version control

## Future Improvements

- [ ] GraphQL API
- [ ] WebSocket for real-time updates
- [ ] Microservices architecture
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Performance monitoring
- [ ] Security audits

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Celery Docs](https://docs.celeryq.dev/)
