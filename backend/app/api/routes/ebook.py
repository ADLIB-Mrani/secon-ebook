"""E-book API routes."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models import Ebook, Resource, EbookStatus, EbookFormat, ResourceType
from app.services.tasks import generate_ebook_task
from app.services.content_processor import content_processor
from app.utils.file_handler import save_upload_file, extract_text_from_file
from app.core.config import settings
import os
from datetime import datetime

router = APIRouter(prefix="/ebook", tags=["ebook"])


# Pydantic schemas
class EbookCreate(BaseModel):
    title: str
    author: str = "Unknown"
    description: Optional[str] = None
    format: str = "epub"
    template_id: Optional[int] = None


class EbookResponse(BaseModel):
    id: int
    title: str
    author: str
    status: str
    format: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResourceCreate(BaseModel):
    type: str
    source: str
    title: Optional[str] = None
    order: int = 0


class GenerateRequest(BaseModel):
    chapters: Optional[List[dict]] = None
    auto_extract: bool = True


@router.post("/create", response_model=EbookResponse)
def create_ebook(ebook_data: EbookCreate, db: Session = Depends(get_db)):
    """Create a new e-book project."""
    try:
        ebook = Ebook(
            title=ebook_data.title,
            author=ebook_data.author,
            description=ebook_data.description,
            format=EbookFormat(ebook_data.format),
            status=EbookStatus.DRAFT,
            template_id=ebook_data.template_id
        )
        
        db.add(ebook)
        db.commit()
        db.refresh(ebook)
        
        return ebook
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ebook_id}", response_model=EbookResponse)
def get_ebook(ebook_id: int, db: Session = Depends(get_db)):
    """Get e-book details."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    return ebook


@router.post("/{ebook_id}/resources")
def add_resource(ebook_id: int, resource_data: ResourceCreate, db: Session = Depends(get_db)):
    """Add a resource to an e-book."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    try:
        resource = Resource(
            ebook_id=ebook_id,
            type=ResourceType(resource_data.type),
            source=resource_data.source,
            title=resource_data.title,
            order=resource_data.order
        )
        
        db.add(resource)
        db.commit()
        db.refresh(resource)
        
        return {"id": resource.id, "message": "Resource added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ebook_id}/upload")
async def upload_file(
    ebook_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a file as a resource."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    try:
        # Save file
        file_path = os.path.join(settings.TEMP_DIR, f"{ebook_id}_{file.filename}")
        await save_upload_file(file, file_path)
        
        # Extract text content
        content = extract_text_from_file(file_path)
        
        # Create resource
        resource = Resource(
            ebook_id=ebook_id,
            type=ResourceType.FILE,
            source=file_path,
            title=file.filename,
            content=content
        )
        
        db.add(resource)
        db.commit()
        
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ebook_id}/generate")
def generate_ebook(
    ebook_id: int,
    generate_data: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate e-book from resources."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    try:
        # Get resources
        resources = db.query(Resource).filter(Resource.ebook_id == ebook_id).order_by(Resource.order).all()
        
        if not resources:
            raise HTTPException(status_code=400, detail="No resources found")
        
        # Prepare chapters
        if generate_data.chapters:
            chapters = generate_data.chapters
        else:
            # Auto-extract chapters from resources
            chapters = []
            for resource in resources:
                if resource.content:
                    extracted = content_processor.extract_chapters(resource.content)
                    chapters.extend(extracted)
                else:
                    chapters.append({
                        'title': resource.title or 'Untitled',
                        'content': resource.source
                    })
        
        # Set output path
        output_filename = f"{ebook.title.replace(' ', '_')}_{ebook_id}.{ebook.format.value}"
        output_path = os.path.join(settings.OUTPUT_DIR, output_filename)
        
        # Update status
        ebook.status = EbookStatus.PROCESSING
        db.commit()
        
        # Start async task
        task = generate_ebook_task.delay(
            ebook_id=ebook_id,
            title=ebook.title,
            author=ebook.author,
            chapters=chapters,
            output_format=ebook.format.value,
            output_path=output_path
        )
        
        # Save task ID
        ebook.task_id = task.id
        db.commit()
        
        return {
            "message": "E-book generation started",
            "task_id": task.id,
            "status": "processing"
        }
    except Exception as e:
        ebook.status = EbookStatus.FAILED
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ebook_id}/status")
def get_generation_status(ebook_id: int, db: Session = Depends(get_db)):
    """Get e-book generation status."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    if not ebook.task_id:
        return {"status": ebook.status.value}
    
    # Check task status
    from app.core.celery_app import celery_app
    task = celery_app.AsyncResult(ebook.task_id)
    
    if task.state == 'SUCCESS':
        ebook.status = EbookStatus.COMPLETED
        ebook.output_path = task.result.get('output_path')
        db.commit()
    elif task.state == 'FAILURE':
        ebook.status = EbookStatus.FAILED
        db.commit()
    
    return {
        "status": task.state,
        "ebook_status": ebook.status.value,
        "info": task.info if task.info else None
    }


@router.get("/{ebook_id}/download")
def download_ebook(ebook_id: int, db: Session = Depends(get_db)):
    """Get download URL for generated e-book."""
    from fastapi.responses import FileResponse
    
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    if ebook.status != EbookStatus.COMPLETED or not ebook.output_path:
        raise HTTPException(status_code=400, detail="E-book not ready for download")
    
    if not os.path.exists(ebook.output_path):
        raise HTTPException(status_code=404, detail="E-book file not found")
    
    return FileResponse(
        ebook.output_path,
        filename=os.path.basename(ebook.output_path),
        media_type='application/octet-stream'
    )


@router.delete("/{ebook_id}")
def delete_ebook(ebook_id: int, db: Session = Depends(get_db)):
    """Delete an e-book project."""
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    
    if not ebook:
        raise HTTPException(status_code=404, detail="E-book not found")
    
    try:
        # Delete file if exists
        if ebook.output_path and os.path.exists(ebook.output_path):
            os.remove(ebook.output_path)
        
        db.delete(ebook)
        db.commit()
        
        return {"message": "E-book deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[EbookResponse])
def list_ebooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all e-books."""
    ebooks = db.query(Ebook).offset(skip).limit(limit).all()
    return ebooks
