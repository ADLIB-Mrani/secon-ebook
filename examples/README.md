# Example E-books

This directory contains example e-books and content to help you get started.

## Sample Content

### sample-content.md

A comprehensive example showing all the features of Secon E-book Generator. This file demonstrates:

- Multiple chapters with structured content
- Different heading levels
- Lists (ordered and unordered)
- Code examples
- Best practices
- Use cases

## Using the Examples

### Generate from Sample Content

1. Start the application:
   ```bash
   docker-compose up -d
   ```

2. Navigate to http://localhost:3000

3. Create a new e-book

4. Upload `sample-content.md` 

5. Choose a template (e.g., "Technical Manual")

6. Generate and download!

### Via API

```bash
# Create e-book
EBOOK_ID=$(curl -s -X POST http://localhost:8000/api/v1/ebook/create \
  -H "Content-Type: application/json" \
  -d '{"title": "Example Book", "author": "Secon", "format": "epub"}' \
  | jq -r '.id')

# Upload sample content
curl -X POST http://localhost:8000/api/v1/ebook/$EBOOK_ID/upload \
  -F "file=@sample-content.md"

# Generate
curl -X POST http://localhost:8000/api/v1/ebook/$EBOOK_ID/generate \
  -H "Content-Type: application/json" \
  -d '{"auto_extract": true}'

# Wait a bit...
sleep 30

# Download
curl http://localhost:8000/api/v1/ebook/$EBOOK_ID/download -o example.epub
```

## Creating Your Own

### From Blog Posts

```bash
# Example: Scrape a blog
curl -X POST http://localhost:8000/api/v1/resources/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/post", "use_playwright": false}'
```

### From Multiple Sources

1. Create e-book
2. Add multiple files/URLs
3. Let the system organize them
4. Generate

## Templates Showcase

Try different templates with the same content:

- **Novel**: Fiction-style layout
- **Technical Manual**: Code-friendly
- **Magazine**: Visual, modern
- **Academic**: Formal, structured

## Tips

- Start with sample-content.md to understand the structure
- Experiment with different templates
- Try different output formats
- Customize based on your needs

## Next Steps

- Read [User Guide](../docs/USER_GUIDE.md)
- Check [API Documentation](http://localhost:8000/docs)
- Explore [Templates](../docs/USER_GUIDE.md#templates)

---

Happy e-booking! 📚
