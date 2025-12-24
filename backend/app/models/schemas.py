from pydantic import BaseModel
from typing import List, Optional, Literal

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class Citation(BaseModel):
    id: int
    document: str
    page: int
    text: str

class Source(BaseModel):
    id: int
    title: str
    document: str
    page: int

class ChatResponse(BaseModel):
    job_id: str
    message: str

class StreamEvent(BaseModel):
    type: Literal["text", "tool_call", "citation", "source", "component", "done", "error"]
    content: Optional[str] = None
    data: Optional[dict] = None
