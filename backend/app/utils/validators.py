"""Input validation utilities."""
from typing import List, Optional
from pydantic import BaseModel, validator, HttpUrl
import re


class URLInput(BaseModel):
    """Validation for URL input."""
    url: HttpUrl
    use_playwright: bool = False


class FileUploadValidation(BaseModel):
    """Validation for file uploads."""
    filename: str
    size: int
    
    @validator('size')
    def validate_size(cls, v):
        max_size = 52428800  # 50MB
        if v > max_size:
            raise ValueError(f'File size must be less than {max_size} bytes')
        return v
    
    @validator('filename')
    def validate_extension(cls, v):
        allowed = ['pdf', 'docx', 'txt', 'md', 'html', 'epub']
        ext = v.split('.')[-1].lower()
        if ext not in allowed:
            raise ValueError(f'File type .{ext} not allowed. Allowed types: {", ".join(allowed)}')
        return v


class EbookCreateInput(BaseModel):
    """Validation for e-book creation."""
    title: str
    author: Optional[str] = "Unknown"
    description: Optional[str] = None
    format: str = "epub"
    
    @validator('title')
    def validate_title(cls, v):
        if len(v) < 1:
            raise ValueError('Title cannot be empty')
        if len(v) > 255:
            raise ValueError('Title too long (max 255 characters)')
        return v
    
    @validator('format')
    def validate_format(cls, v):
        allowed = ['epub', 'pdf', 'mobi', 'html']
        if v.lower() not in allowed:
            raise ValueError(f'Format must be one of: {", ".join(allowed)}')
        return v.lower()


class ResourceInput(BaseModel):
    """Validation for resource input."""
    type: str
    source: str
    title: Optional[str] = None
    order: int = 0
    
    @validator('type')
    def validate_type(cls, v):
        allowed = ['url', 'file', 'text', 'api']
        if v.lower() not in allowed:
            raise ValueError(f'Type must be one of: {", ".join(allowed)}')
        return v.lower()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Remove any directory path
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove special characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    
    # Remove leading dots and spaces
    filename = filename.lstrip('. ')
    
    return filename


def validate_url(url: str) -> bool:
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None
