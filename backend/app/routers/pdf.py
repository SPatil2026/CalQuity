from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.pdf_service import pdf_service
import os

router = APIRouter(prefix="/api/pdf", tags=["pdf"])

@router.get("/{filename}")
async def get_pdf(filename: str):
    """Serve PDF file"""
    pdf_path = pdf_service.get_pdf_path(filename)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@router.get("")
async def list_pdfs():
    """List all available PDFs"""
    return {"documents": pdf_service.list_documents()}

@router.post("/reload")
async def reload_pdfs():
    """Reload PDFs from directory"""
    count = pdf_service.reload_pdfs()
    return {"message": f"Reloaded {count} PDFs", "documents": pdf_service.list_documents()}
