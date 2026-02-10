"""Template API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models import Template

router = APIRouter(prefix="/templates", tags=["templates"])


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    config: Optional[dict] = None
    is_default: bool = False


class TemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    config: Optional[dict]
    is_default: bool
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TemplateResponse])
def list_templates(db: Session = Depends(get_db)):
    """List all templates."""
    templates = db.query(Template).all()
    return templates


@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Get template details."""
    template = db.query(Template).filter(Template.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template


@router.post("/", response_model=TemplateResponse)
def create_template(template_data: TemplateCreate, db: Session = Depends(get_db)):
    """Create a new template."""
    try:
        template = Template(
            name=template_data.name,
            description=template_data.description,
            category=template_data.category,
            config=template_data.config,
            is_default=1 if template_data.is_default else 0
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return template
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def init_default_templates(db: Session):
    """Initialize default templates."""
    default_templates = [
        {
            "name": "Novel",
            "description": "Classic novel template with elegant formatting",
            "category": "fiction",
            "config": {
                "font": "Georgia",
                "font_size": 12,
                "line_height": 1.6,
                "chapter_start": "always_new_page",
                "header": {"show": True, "content": "title"},
                "footer": {"show": True, "content": "page_number"}
            },
            "is_default": 1
        },
        {
            "name": "Technical Manual",
            "description": "Technical documentation template with code highlighting",
            "category": "technical",
            "config": {
                "font": "Arial",
                "font_size": 11,
                "line_height": 1.5,
                "chapter_start": "new_page",
                "code_highlighting": True,
                "table_of_contents": True,
                "header": {"show": True, "content": "chapter_title"},
                "footer": {"show": True, "content": "page_number"}
            },
            "is_default": 0
        },
        {
            "name": "Magazine",
            "description": "Magazine-style layout with columns",
            "category": "magazine",
            "config": {
                "font": "Helvetica",
                "font_size": 10,
                "line_height": 1.4,
                "columns": 2,
                "image_placement": "inline",
                "header": {"show": True, "content": "magazine_name"},
                "footer": {"show": False}
            },
            "is_default": 0
        },
        {
            "name": "Academic Paper",
            "description": "Academic paper format with citations",
            "category": "academic",
            "config": {
                "font": "Times New Roman",
                "font_size": 12,
                "line_height": 2.0,
                "chapter_start": "new_page",
                "citations": True,
                "bibliography": True,
                "header": {"show": True, "content": "title"},
                "footer": {"show": True, "content": "page_number"}
            },
            "is_default": 0
        }
    ]
    
    for template_data in default_templates:
        existing = db.query(Template).filter(Template.name == template_data["name"]).first()
        if not existing:
            template = Template(**template_data)
            db.add(template)
    
    db.commit()
