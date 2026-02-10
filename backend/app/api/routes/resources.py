"""Resource management API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.services.scraper import scraper_service
from app.services.api_integrations import api_service
from app.utils.validators import URLInput

router = APIRouter(prefix="/resources", tags=["resources"])


class ScrapeResponse(BaseModel):
    title: str
    content: str
    url: str
    success: bool
    images: Optional[list] = []


class ImageSearchRequest(BaseModel):
    query: str
    count: int = 5


class BookSearchRequest(BaseModel):
    query: str
    max_results: int = 10


@router.post("/scrape", response_model=ScrapeResponse)
def scrape_url(url_data: URLInput):
    """Scrape content from a URL."""
    try:
        result = scraper_service.scrape_url(
            str(url_data.url),
            use_playwright=url_data.use_playwright
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/search")
def search_images(request: ImageSearchRequest):
    """Search for images using Unsplash API."""
    try:
        images = api_service.search_images(request.query, request.count)
        return {"images": images, "count": len(images)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/books/search")
def search_books(request: BookSearchRequest):
    """Search for books using Google Books API."""
    try:
        books = api_service.search_books(request.query, request.max_results)
        return {"books": books, "count": len(books)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/archive/search")
def search_archive(query: str, media_type: str = "texts"):
    """Search Archive.org for free resources."""
    try:
        results = api_service.search_archive(query, media_type)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/content/summarize")
def summarize_content(text: str, max_length: int = 130):
    """Summarize text using AI."""
    try:
        summary = api_service.summarize_text(text, max_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
