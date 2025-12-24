from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Now import routers (which import services)
from app.routers import chat, pdf

app = FastAPI(title="AI Search Chat API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(pdf.router)

@app.get("/")
async def root():
    return {"message": "AI Search Chat API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
