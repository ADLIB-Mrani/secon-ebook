"""Content processing utilities."""
import re
import markdown
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class ContentProcessor:
    """Process and clean content for e-book generation."""
    
    def clean_html(self, html: str) -> str:
        """Clean and sanitize HTML content."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted tags
        for tag in soup(['script', 'style', 'iframe', 'noscript']):
            tag.decompose()
        
        # Clean attributes
        for tag in soup.find_all(True):
            tag.attrs = {key: value for key, value in tag.attrs.items() 
                        if key in ['href', 'src', 'alt', 'title']}
        
        return str(soup)
    
    def markdown_to_html(self, md_content: str) -> str:
        """Convert Markdown to HTML."""
        return markdown.markdown(
            md_content,
            extensions=['extra', 'codehilite', 'toc', 'tables']
        )
    
    def extract_chapters(self, content: str, by_h1: bool = True) -> List[Dict[str, str]]:
        """
        Extract chapters from content based on headers.
        
        Args:
            content: HTML or text content
            by_h1: Split by h1 tags if True, otherwise by h2
            
        Returns:
            List of chapters with title and content
        """
        soup = BeautifulSoup(content, 'html.parser')
        chapters = []
        
        header_tag = 'h1' if by_h1 else 'h2'
        headers = soup.find_all(header_tag)
        
        if not headers:
            # No headers found, return as single chapter
            return [{
                'title': 'Content',
                'content': str(soup)
            }]
        
        for i, header in enumerate(headers):
            title = header.get_text().strip()
            
            # Get content until next header
            content_parts = []
            for sibling in header.find_next_siblings():
                if sibling.name == header_tag:
                    break
                content_parts.append(str(sibling))
            
            chapters.append({
                'title': title,
                'content': ''.join(content_parts)
            })
        
        return chapters
    
    def add_table_of_contents(self, chapters: List[Dict[str, str]]) -> str:
        """Generate HTML table of contents."""
        toc = '<div class="toc"><h2>Table of Contents</h2><ol>'
        
        for i, chapter in enumerate(chapters, 1):
            toc += f'<li><a href="#chapter-{i}">{chapter["title"]}</a></li>'
        
        toc += '</ol></div>'
        return toc
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that cause issues
        text = text.replace('\u200b', '')  # Zero-width space
        text = text.replace('\ufeff', '')  # BOM
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n')
        
        return text.strip()
    
    def split_long_content(self, content: str, max_length: int = 10000) -> List[str]:
        """Split long content into smaller chunks."""
        if len(content) <= max_length:
            return [content]
        
        chunks = []
        paragraphs = content.split('\n\n')
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para)
            
            if current_length + para_length > max_length and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def enhance_content(self, content: str, add_formatting: bool = True) -> str:
        """Enhance content with better formatting."""
        if not add_formatting:
            return content
        
        # Wrap paragraphs in <p> tags if not already
        soup = BeautifulSoup(content, 'html.parser')
        
        if not soup.find('p'):
            paragraphs = content.split('\n\n')
            content = '\n'.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
        
        return content


# Singleton instance
content_processor = ContentProcessor()
