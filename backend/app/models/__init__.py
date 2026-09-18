from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EbookStatus(str, enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EbookFormat(str, enum.Enum):
    EPUB = "epub"
    PDF = "pdf"
    MOBI = "mobi"
    HTML = "html"
    DOCX = "docx"


class Ebook(Base):
    """E-book project model."""
    __tablename__ = "ebooks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    author = Column(String(255))
    status = Column(Enum(EbookStatus), default=EbookStatus.DRAFT)
    format = Column(Enum(EbookFormat), default=EbookFormat.EPUB)
    template_id = Column(Integer, ForeignKey("templates.id"))
    cover_image_url = Column(String(500))
    metadata = Column(JSON)  # Additional metadata
    output_path = Column(String(500))
    task_id = Column(String(255))  # Celery task ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    resources = relationship("Resource", back_populates="ebook", cascade="all, delete-orphan")
    template = relationship("Template", back_populates="ebooks")


class ResourceType(str, enum.Enum):
    URL = "url"
    FILE = "file"
    TEXT = "text"
    API = "api"


class Resource(Base):
    """Content resource model."""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    ebook_id = Column(Integer, ForeignKey("ebooks.id"), nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    source = Column(Text, nullable=False)  # URL, file path, or text content
    title = Column(String(255))
    content = Column(Text)
    metadata = Column(JSON)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ebook = relationship("Ebook", back_populates="resources")


class Template(Base):
    """E-book template model."""
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    category = Column(String(100))  # novel, technical, magazine, etc.
    config = Column(JSON)  # Template configuration (fonts, colors, layout)
    is_default = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ebooks = relationship("Ebook", back_populates="template")


class User(Base):
    """User model for future authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
