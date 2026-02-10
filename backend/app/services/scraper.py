"""Web scraping service using BeautifulSoup and Playwright."""
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import logging

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for scraping web content."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_url(self, url: str, use_playwright: bool = False) -> Dict[str, Any]:
        """
        Scrape content from a URL.
        
        Args:
            url: The URL to scrape
            use_playwright: Whether to use Playwright for JavaScript rendering
            
        Returns:
            Dictionary with scraped content and metadata
        """
        try:
            if use_playwright:
                return self._scrape_with_playwright(url)
            else:
                return self._scrape_with_beautifulsoup(url)
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise
    
    def _scrape_with_beautifulsoup(self, url: str) -> Dict[str, Any]:
        """Scrape using BeautifulSoup (for static HTML)."""
        try:
            # Try using newspaper3k first for article extraction
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                "title": article.title,
                "content": article.text,
                "html": article.html,
                "authors": article.authors,
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                "top_image": article.top_image,
                "images": list(article.images),
                "url": url,
                "success": True
            }
        except Exception as e:
            logger.warning(f"Newspaper3k failed, falling back to BeautifulSoup: {str(e)}")
            
            # Fallback to BeautifulSoup
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title = title.get_text() if title else urlparse(url).netloc
            
            # Extract main content (try common content containers)
            content_div = (
                soup.find('article') or 
                soup.find('main') or 
                soup.find('div', class_='content') or
                soup.find('div', id='content') or
                soup.body
            )
            
            content = content_div.get_text(separator='\n\n', strip=True) if content_div else ""
            
            # Extract images
            images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
            
            return {
                "title": title.strip(),
                "content": content,
                "html": str(soup),
                "images": images,
                "url": url,
                "success": True
            }
    
    def _scrape_with_playwright(self, url: str) -> Dict[str, Any]:
        """Scrape using Playwright (for JavaScript-rendered content)."""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle")
                
                # Wait for content to load
                page.wait_for_timeout(2000)
                
                # Extract content
                content = page.evaluate("""
                    () => {
                        const article = document.querySelector('article') || 
                                      document.querySelector('main') ||
                                      document.querySelector('.content') ||
                                      document.body;
                        return article ? article.innerText : '';
                    }
                """)
                
                title = page.title()
                html = page.content()
                
                browser.close()
                
                return {
                    "title": title,
                    "content": content,
                    "html": html,
                    "url": url,
                    "success": True
                }
        except ImportError:
            logger.error("Playwright not installed. Install with: pip install playwright && playwright install")
            raise
        except Exception as e:
            logger.error(f"Playwright scraping failed: {str(e)}")
            raise
    
    def extract_metadata(self, html: str) -> Dict[str, Any]:
        """Extract metadata from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        metadata = {}
        
        # Open Graph metadata
        for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            key = meta.get('property', '').replace('og:', '')
            metadata[key] = meta.get('content', '')
        
        # Twitter Card metadata
        for meta in soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')}):
            key = meta.get('name', '').replace('twitter:', '')
            metadata[key] = meta.get('content', '')
        
        # Standard metadata
        for meta in soup.find_all('meta', attrs={'name': True}):
            metadata[meta.get('name')] = meta.get('content', '')
        
        return metadata


# Singleton instance
scraper_service = ScraperService()
