import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, ChatResponse
from app.services.queue_service import queue_service
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def create_chat(request: ChatRequest):
    """Create a new chat request and return job ID"""
    job_id = queue_service.create_job(request.message)
    return ChatResponse(job_id=job_id, message="Job created")

@router.get("/stream/{job_id}")
async def stream_response(job_id: str):
    """Stream AI response using SSE"""
    job = queue_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    async def event_generator():
        try:
            async for event in ai_service.generate_response(job.message):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            error_event = {"type": "error", "content": str(e)}
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
