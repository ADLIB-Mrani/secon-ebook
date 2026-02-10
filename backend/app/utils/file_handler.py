"""File handling utilities."""
import os
import shutil
from typing import Optional
from pathlib import Path
import aiofiles
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)


async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to disk.
    
    Args:
        upload_file: The uploaded file
        destination: Destination path
        
    Returns:
        Path to saved file
    """
    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        async with aiofiles.open(destination, 'wb') as f:
            content = await upload_file.read()
            await f.write(content)
        
        logger.info(f"File saved: {destination}")
        return destination
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise


def get_file_extension(filename: str) -> str:
    """Get file extension without the dot."""
    return Path(filename).suffix[1:].lower()


def is_allowed_file(filename: str, allowed_extensions: list) -> bool:
    """Check if file extension is allowed."""
    extension = get_file_extension(filename)
    return extension in allowed_extensions


def create_unique_filename(original_filename: str, directory: str) -> str:
    """Create a unique filename to avoid conflicts."""
    base_name = Path(original_filename).stem
    extension = Path(original_filename).suffix
    counter = 1
    
    new_filename = original_filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return new_filename


def cleanup_temp_files(directory: str, max_age_hours: int = 24):
    """Clean up temporary files older than max_age_hours."""
    import time
    
    try:
        now = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_age = now - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    logger.info(f"Removed old temp file: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning temp files: {str(e)}")


def extract_text_from_file(filepath: str) -> str:
    """Extract text content from various file formats."""
    extension = get_file_extension(filepath)
    
    try:
        if extension == 'txt' or extension == 'md':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif extension == 'pdf':
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(filepath)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                return '\n\n'.join(text)
            except Exception as e:
                logger.error(f"Error extracting PDF: {str(e)}")
                return ""
        
        elif extension == 'docx':
            try:
                from docx import Document
                doc = Document(filepath)
                return '\n\n'.join([para.text for para in doc.paragraphs])
            except Exception as e:
                logger.error(f"Error extracting DOCX: {str(e)}")
                return ""
        
        elif extension == 'html' or extension == 'htm':
            with open(filepath, 'r', encoding='utf-8') as f:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(f.read(), 'html.parser')
                return soup.get_text()
        
        else:
            logger.warning(f"Unsupported file type: {extension}")
            return ""
    
    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {str(e)}")
        return ""
