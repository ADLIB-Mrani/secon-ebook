"""Basic tests for backend services."""
import pytest
from app.services.content_processor import ContentProcessor
from app.services.ebook_generator import EbookGeneratorService


class TestContentProcessor:
    """Test content processing functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.processor = ContentProcessor()
    
    def test_clean_html(self):
        """Test HTML cleaning."""
        html = '<div><script>alert("bad")</script><p>Good content</p></div>'
        cleaned = self.processor.clean_html(html)
        
        assert '<script>' not in cleaned
        assert 'Good content' in cleaned
    
    def test_markdown_to_html(self):
        """Test Markdown conversion."""
        md = '# Hello\n\nThis is **bold** text.'
        html = self.processor.markdown_to_html(md)
        
        assert '<h1>' in html
        assert '<strong>' in html or '<b>' in html
    
    def test_clean_text(self):
        """Test text cleaning."""
        text = '  Hello   World  \n\n\n  '
        cleaned = self.processor.clean_text(text)
        
        assert cleaned == 'Hello World'
    
    def test_extract_chapters_with_h1(self):
        """Test chapter extraction."""
        html = '''
        <h1>Chapter 1</h1>
        <p>Content 1</p>
        <h1>Chapter 2</h1>
        <p>Content 2</p>
        '''
        chapters = self.processor.extract_chapters(html, by_h1=True)
        
        assert len(chapters) == 2
        assert chapters[0]['title'] == 'Chapter 1'
        assert chapters[1]['title'] == 'Chapter 2'


class TestEbookGenerator:
    """Test e-book generation functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = EbookGeneratorService()
    
    def test_generate_html(self, tmp_path):
        """Test HTML generation."""
        output = tmp_path / "test.html"
        chapters = [
            {'title': 'Chapter 1', 'content': '<p>Test content</p>'}
        ]
        
        result = self.generator.generate_html(
            title='Test Book',
            author='Test Author',
            chapters=chapters,
            output_path=str(output)
        )
        
        assert output.exists()
        assert 'Test Book' in output.read_text()


@pytest.fixture
def sample_ebook_data():
    """Sample e-book data for testing."""
    return {
        'title': 'Test E-book',
        'author': 'Test Author',
        'chapters': [
            {
                'title': 'Introduction',
                'content': '<p>This is the introduction.</p>'
            },
            {
                'title': 'Chapter 1',
                'content': '<p>This is chapter 1.</p>'
            }
        ]
    }


def test_sample_data_structure(sample_ebook_data):
    """Test sample data structure."""
    assert 'title' in sample_ebook_data
    assert 'author' in sample_ebook_data
    assert len(sample_ebook_data['chapters']) == 2
