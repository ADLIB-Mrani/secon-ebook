"""E-book generation service supporting multiple formats."""
import os
import tempfile
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class EbookGeneratorService:
    """Service for generating e-books in various formats."""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def generate_epub(
        self,
        title: str,
        author: str,
        chapters: List[Dict[str, str]],
        output_path: str,
        cover_image: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate EPUB e-book.
        
        Args:
            title: Book title
            author: Book author
            chapters: List of chapters with 'title' and 'content'
            output_path: Output file path
            cover_image: Path to cover image
            metadata: Additional metadata
            
        Returns:
            Path to generated EPUB file
        """
        try:
            from ebooklib import epub
            
            book = epub.EpubBook()
            
            # Set metadata
            book.set_identifier(f'ebook_{datetime.now().timestamp()}')
            book.set_title(title)
            book.set_language('en')
            book.add_author(author)
            
            if metadata:
                if 'description' in metadata:
                    book.add_metadata('DC', 'description', metadata['description'])
                if 'publisher' in metadata:
                    book.add_metadata('DC', 'publisher', metadata['publisher'])
                if 'date' in metadata:
                    book.add_metadata('DC', 'date', metadata['date'])
            
            # Add cover image
            if cover_image and os.path.exists(cover_image):
                with open(cover_image, 'rb') as f:
                    book.set_cover('cover.jpg', f.read())
            
            # Create chapters
            epub_chapters = []
            toc = []
            spine = ['nav']
            
            for idx, chapter_data in enumerate(chapters):
                chapter = epub.EpubHtml(
                    title=chapter_data.get('title', f'Chapter {idx + 1}'),
                    file_name=f'chapter_{idx + 1}.xhtml',
                    lang='en'
                )
                
                chapter.content = f'''
                <html>
                <head>
                    <title>{chapter_data.get('title', f'Chapter {idx + 1}')}</title>
                </head>
                <body>
                    <h1>{chapter_data.get('title', f'Chapter {idx + 1}')}</h1>
                    <div>{chapter_data.get('content', '')}</div>
                </body>
                </html>
                '''
                
                book.add_item(chapter)
                epub_chapters.append(chapter)
                toc.append(chapter)
                spine.append(chapter)
            
            # Add default NCX and Nav
            book.toc = toc
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            
            # Define CSS style
            style = '''
            body { font-family: Georgia, serif; margin: 2em; }
            h1 { color: #333; margin-top: 2em; }
            p { text-align: justify; margin: 1em 0; }
            '''
            nav_css = epub.EpubItem(
                uid="style_nav",
                file_name="style/nav.css",
                media_type="text/css",
                content=style
            )
            book.add_item(nav_css)
            
            # Basic spine
            book.spine = spine
            
            # Write EPUB file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            epub.write_epub(output_path, book, {})
            
            logger.info(f"EPUB generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating EPUB: {str(e)}")
            raise
    
    def generate_pdf(
        self,
        title: str,
        author: str,
        chapters: List[Dict[str, str]],
        output_path: str,
        cover_image: Optional[str] = None
    ) -> str:
        """
        Generate PDF e-book using WeasyPrint.
        
        Args:
            title: Book title
            author: Book author
            chapters: List of chapters
            output_path: Output file path
            cover_image: Path to cover image
            
        Returns:
            Path to generated PDF file
        """
        try:
            from weasyprint import HTML, CSS
            
            # Build HTML content
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                        @top-center {{
                            content: "{title}";
                            font-size: 9pt;
                            color: #666;
                        }}
                        @bottom-center {{
                            content: counter(page);
                            font-size: 9pt;
                        }}
                    }}
                    body {{
                        font-family: 'Georgia', serif;
                        font-size: 11pt;
                        line-height: 1.6;
                        color: #333;
                    }}
                    h1 {{
                        font-size: 24pt;
                        margin-top: 2cm;
                        margin-bottom: 1cm;
                        page-break-before: always;
                    }}
                    h1:first-of-type {{
                        page-break-before: avoid;
                    }}
                    p {{
                        text-align: justify;
                        margin: 1em 0;
                    }}
                    .cover {{
                        page-break-after: always;
                        text-align: center;
                        padding-top: 5cm;
                    }}
                    .cover h1 {{
                        font-size: 36pt;
                        margin-top: 0;
                        page-break-before: avoid;
                    }}
                    .cover p {{
                        font-size: 18pt;
                        margin-top: 2cm;
                    }}
                </style>
            </head>
            <body>
                <div class="cover">
                    <h1>{title}</h1>
                    <p>by {author}</p>
                </div>
            '''
            
            # Add chapters
            for chapter in chapters:
                chapter_title = chapter.get('title', 'Untitled Chapter')
                chapter_content = chapter.get('content', '')
                
                html_content += f'''
                <div class="chapter">
                    <h1>{chapter_title}</h1>
                    <div>{chapter_content}</div>
                </div>
                '''
            
            html_content += '''
            </body>
            </html>
            '''
            
            # Generate PDF
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            HTML(string=html_content).write_pdf(output_path)
            
            logger.info(f"PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    def convert_to_mobi(self, epub_path: str, output_path: str) -> str:
        """
        Convert EPUB to MOBI using ebook-convert (Calibre).
        Note: Requires Calibre to be installed.
        
        Args:
            epub_path: Path to EPUB file
            output_path: Output MOBI file path
            
        Returns:
            Path to generated MOBI file
        """
        try:
            import subprocess
            
            # Check if ebook-convert is available
            result = subprocess.run(
                ['ebook-convert', epub_path, output_path],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"MOBI generated successfully: {output_path}")
                return output_path
            else:
                raise Exception(f"ebook-convert failed: {result.stderr}")
                
        except FileNotFoundError:
            logger.error("ebook-convert not found. Please install Calibre.")
            raise Exception("Calibre not installed. MOBI conversion requires Calibre.")
        except Exception as e:
            logger.error(f"Error generating MOBI: {str(e)}")
            raise
    
    def generate_html(
        self,
        title: str,
        author: str,
        chapters: List[Dict[str, str]],
        output_path: str
    ) -> str:
        """Generate standalone HTML e-book."""
        try:
            html_content = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: 'Georgia', serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 2rem;
                        line-height: 1.8;
                        color: #333;
                    }}
                    h1 {{ color: #2c3e50; margin-top: 2rem; }}
                    .cover {{
                        text-align: center;
                        padding: 4rem 0;
                        border-bottom: 2px solid #eee;
                        margin-bottom: 3rem;
                    }}
                    .cover h1 {{ font-size: 3rem; margin: 0; }}
                    .cover p {{ font-size: 1.5rem; color: #666; }}
                    .chapter {{ margin: 2rem 0; }}
                    p {{ text-align: justify; }}
                </style>
            </head>
            <body>
                <div class="cover">
                    <h1>{title}</h1>
                    <p>by {author}</p>
                </div>
            '''
            
            for chapter in chapters:
                html_content += f'''
                <div class="chapter">
                    <h1>{chapter.get('title', 'Untitled')}</h1>
                    <div>{chapter.get('content', '')}</div>
                </div>
                '''
            
            html_content += '''
            </body>
            </html>
            '''
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating HTML: {str(e)}")
            raise


# Singleton instance
ebook_generator = EbookGeneratorService()
