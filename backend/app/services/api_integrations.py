"""API integration services for external APIs."""
import requests
from typing import Dict, Any, List, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class APIIntegrationService:
    """Service for integrating with external APIs."""
    
    def __init__(self):
        self.huggingface_key = settings.HUGGINGFACE_API_KEY
        self.unsplash_key = settings.UNSPLASH_ACCESS_KEY
        self.google_books_key = settings.GOOGLE_BOOKS_API_KEY
        self.rapidapi_key = settings.RAPIDAPI_KEY
    
    # Hugging Face API
    def summarize_text(self, text: str, max_length: int = 130) -> str:
        """Summarize text using Hugging Face API."""
        if not self.huggingface_key:
            logger.warning("Hugging Face API key not set")
            return text[:500] + "..."
        
        try:
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": f"Bearer {self.huggingface_key}"}
            
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text[:1024], "parameters": {"max_length": max_length}},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result[0]["summary_text"] if isinstance(result, list) else text
            else:
                logger.error(f"Hugging Face API error: {response.status_code}")
                return text[:500] + "..."
        except Exception as e:
            logger.error(f"Error in summarize_text: {str(e)}")
            return text[:500] + "..."
    
    def translate_text(self, text: str, target_lang: str = "en") -> str:
        """Translate text using Hugging Face API."""
        if not self.huggingface_key:
            return text
        
        try:
            API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr"
            headers = {"Authorization": f"Bearer {self.huggingface_key}"}
            
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text[:1024]},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result[0]["translation_text"] if isinstance(result, list) else text
            return text
        except Exception as e:
            logger.error(f"Error in translate_text: {str(e)}")
            return text
    
    # Unsplash API
    def search_images(self, query: str, count: int = 5) -> List[Dict[str, str]]:
        """Search for images on Unsplash."""
        if not self.unsplash_key:
            logger.warning("Unsplash API key not set")
            return []
        
        try:
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": count,
                "client_id": self.unsplash_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "id": img["id"],
                        "url": img["urls"]["regular"],
                        "thumbnail": img["urls"]["thumb"],
                        "description": img.get("description", ""),
                        "author": img["user"]["name"],
                        "download_url": img["links"]["download"]
                    }
                    for img in data.get("results", [])
                ]
            return []
        except Exception as e:
            logger.error(f"Error searching Unsplash: {str(e)}")
            return []
    
    # Google Books API
    def search_books(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for books using Google Books API."""
        try:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                "q": query,
                "maxResults": max_results
            }
            
            if self.google_books_key:
                params["key"] = self.google_books_key
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                books = []
                
                for item in data.get("items", []):
                    volume_info = item.get("volumeInfo", {})
                    books.append({
                        "id": item.get("id"),
                        "title": volume_info.get("title", ""),
                        "authors": volume_info.get("authors", []),
                        "description": volume_info.get("description", ""),
                        "publisher": volume_info.get("publisher", ""),
                        "published_date": volume_info.get("publishedDate", ""),
                        "categories": volume_info.get("categories", []),
                        "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                        "preview_link": volume_info.get("previewLink", "")
                    })
                
                return books
            return []
        except Exception as e:
            logger.error(f"Error searching Google Books: {str(e)}")
            return []
    
    # Archive.org API
    def search_archive(self, query: str, media_type: str = "texts") -> List[Dict[str, Any]]:
        """Search Archive.org for free resources."""
        try:
            url = "https://archive.org/advancedsearch.php"
            params = {
                "q": query,
                "fl[]": ["identifier", "title", "creator", "description", "date"],
                "rows": 20,
                "page": 1,
                "output": "json",
                "mediatype": media_type
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", {}).get("docs", [])
            return []
        except Exception as e:
            logger.error(f"Error searching Archive.org: {str(e)}")
            return []
    
    # OpenLibrary API
    def get_book_details(self, isbn: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
        """Get book details from OpenLibrary."""
        try:
            if isbn:
                url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            elif title:
                url = f"https://openlibrary.org/search.json?title={title}"
            else:
                return {}
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"Error fetching from OpenLibrary: {str(e)}")
            return {}


# Singleton instance
api_service = APIIntegrationService()
