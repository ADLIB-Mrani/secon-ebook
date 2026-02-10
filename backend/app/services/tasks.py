"""Celery tasks for async e-book generation."""
from celery import Task
from app.core.celery_app import celery_app
from app.services.ebook_generator import ebook_generator
from app.services.scraper import scraper_service
from app.services.content_processor import content_processor
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Base task with callbacks."""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure."""
        logger.error(f'Task {task_id} failed: {exc}')
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success."""
        logger.info(f'Task {task_id} succeeded')
        super().on_success(retval, task_id, args, kwargs)


@celery_app.task(base=CallbackTask, bind=True)
def generate_ebook_task(
    self,
    ebook_id: int,
    title: str,
    author: str,
    chapters: List[Dict[str, str]],
    output_format: str,
    output_path: str
):
    """
    Async task to generate e-book.
    
    Args:
        ebook_id: E-book database ID
        title: Book title
        author: Book author
        chapters: List of chapters
        output_format: Output format (epub, pdf, html)
        output_path: Output file path
    """
    try:
        self.update_state(state='PROCESSING', meta={'progress': 10, 'status': 'Starting generation'})
        
        if output_format == 'epub':
            result_path = ebook_generator.generate_epub(
                title=title,
                author=author,
                chapters=chapters,
                output_path=output_path
            )
        elif output_format == 'pdf':
            result_path = ebook_generator.generate_pdf(
                title=title,
                author=author,
                chapters=chapters,
                output_path=output_path
            )
        elif output_format == 'html':
            result_path = ebook_generator.generate_html(
                title=title,
                author=author,
                chapters=chapters,
                output_path=output_path
            )
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'Complete', 'file_path': result_path})
        
        return {
            'status': 'success',
            'ebook_id': ebook_id,
            'output_path': result_path
        }
    
    except Exception as e:
        logger.error(f"Error in generate_ebook_task: {str(e)}")
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise


@celery_app.task(base=CallbackTask)
def scrape_url_task(url: str, use_playwright: bool = False):
    """
    Async task to scrape URL.
    
    Args:
        url: URL to scrape
        use_playwright: Whether to use Playwright
        
    Returns:
        Scraped content
    """
    try:
        result = scraper_service.scrape_url(url, use_playwright)
        return result
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        raise


@celery_app.task(base=CallbackTask)
def process_content_task(content: str, process_type: str = 'clean'):
    """
    Async task to process content.
    
    Args:
        content: Content to process
        process_type: Type of processing (clean, markdown_to_html, extract_chapters)
        
    Returns:
        Processed content
    """
    try:
        if process_type == 'clean':
            return content_processor.clean_html(content)
        elif process_type == 'markdown_to_html':
            return content_processor.markdown_to_html(content)
        elif process_type == 'extract_chapters':
            return content_processor.extract_chapters(content)
        else:
            return content
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")
        raise
