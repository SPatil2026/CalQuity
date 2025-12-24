# AI Search Chat with PDF Citation Viewer

A Perplexity-style chat interface with real-time streaming, citations, and PDF viewer integration.

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ──HTTP──▶│   FastAPI    │ ──────▶│  In-Memory  │
│  (Next.js)  │ ◀──SSE───│   Backend    │ ◀──────│    Queue    │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │                        │
      ▼                        ▼
┌─────────────┐         ┌──────────────┐
│   Zustand   │         │ PDF Service  │
│    Store    │         │  (PyPDF2)    │
└─────────────┘         └──────────────┘
```

### Streaming Protocol

1. **Client** sends message → **Backend** creates job → Returns `job_id`
2. **Client** opens SSE connection with `job_id`
3. **Backend** streams events:
   - `tool_call`: Reasoning steps (thinking, searching, analyzing)
   - `text`: Incremental response chunks
   - `citation`: Citation data with document/page/excerpt
   - `source`: Source card metadata
   - `done`: Stream complete

## Tech Stack

### Frontend
- **Next.js 14.1.0** - App Router, React Server Components
- **TypeScript 5.3.3** - Strict typing
- **Tailwind CSS 3.4.1** - Styling
- **Framer Motion 11.0.3** - Animations (PDF viewer transitions)
- **Zustand 4.5.0** - Global state management
- **React PDF 7.7.0** - PDF rendering

### Backend
- **FastAPI 0.109.0** - REST API & SSE
- **Python 3.11+** - Type hints with Pydantic
- **PyPDF2 3.0.1** - PDF text extraction
- **Uvicorn 0.27.0** - ASGI server
- **asyncio.Queue** - In-memory job queue

## Setup Instructions

### Prerequisites
- Node.js 20+
- Python 3.11+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Add PDF files to pdfs/ directory
# Place your PDF documents in backend/pdfs/

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Docker Setup (Optional)

```bash
# From project root
docker-compose up --build
```

## Environment Variables

### Backend (.env)
```
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
PDF_DIRECTORY=pdfs
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
CalQuilty/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic models
│   │   ├── routers/
│   │   │   ├── chat.py             # Chat & SSE endpoints
│   │   │   └── pdf.py              # PDF serving
│   │   ├── services/
│   │   │   ├── ai_service.py       # AI response generation
│   │   │   ├── pdf_service.py      # PDF processing
│   │   │   └── queue_service.py    # Job queue management
│   │   └── main.py                 # FastAPI app
│   ├── pdfs/                       # PDF documents
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx          # Root layout
│   │   │   ├── page.tsx            # Main page
│   │   │   └── globals.css         # Global styles
│   │   ├── components/
│   │   │   ├── Chat.tsx            # Main chat component
│   │   │   ├── ChatMessage.tsx     # Message display
│   │   │   ├── ChatInput.tsx       # Input field
│   │   │   ├── PDFViewer.tsx       # PDF viewer with animations
│   │   │   └── TypingIndicator.tsx # Loading indicator
│   │   ├── store/
│   │   │   └── chatStore.ts        # Zustand store
│   │   ├── lib/
│   │   │   └── api.ts              # API utilities
│   │   └── types/
│   │       └── index.ts            # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Features Implemented

### ✅ Core Features
- [x] Perplexity-style chat interface
- [x] Real-time streaming with SSE
- [x] Tool call indicators (thinking, searching, analyzing)
- [x] Inline citations [1], [2], etc.
- [x] Source cards with document metadata
- [x] PDF viewer with smooth transitions
- [x] Split-view layout (chat + PDF)
- [x] Responsive design (mobile-first)

### ✅ Streaming
- [x] Text chunks streaming
- [x] Tool call events
- [x] Citation streaming
- [x] Source card streaming
- [x] Typing indicator

### ✅ PDF Features
- [x] PDF text extraction
- [x] Document search
- [x] Page navigation
- [x] Zoom controls
- [x] Animated transitions (300ms slide-in)

### ✅ State Management
- [x] Zustand for global state
- [x] Chat history
- [x] PDF viewer state
- [x] Streaming state

## Design Decisions

### Queue System: In-Memory asyncio.Queue
**Why:** Simplicity for MVP. No external dependencies (Redis/Celery).
**Trade-off:** Not persistent across restarts. For production, use Redis Queue.

### Generative UI: Minimal Implementation
**Why:** Time constraint. Focused on core streaming + citations.
**Trade-off:** Optional components (charts/tables) not implemented. Can extend by adding `component` event type.

### PDF Processing: PyPDF2
**Why:** Lightweight, pure Python, no system dependencies.
**Trade-off:** Limited OCR support. For scanned PDFs, use `pdfplumber` or `pytesseract`.

### Animations: Framer Motion
**Why:** Smooth, declarative animations for PDF viewer transitions.
**Implementation:** 300ms slide-in with scale/fade effect.

### State: Zustand over Redux
**Why:** Minimal boilerplate, TypeScript-friendly, perfect for small-medium apps.

## API Endpoints

### POST `/api/chat`
Create chat job
```json
Request: { "message": "your question" }
Response: { "job_id": "uuid", "message": "Job created" }
```

### GET `/api/chat/stream/{job_id}`
Stream response via SSE
```
Event types: text, tool_call, citation, source, done, error
```

### GET `/api/pdf/{filename}`
Serve PDF file

### GET `/api/pdf`
List available PDFs

## Usage

1. **Add PDFs**: Place PDF files in `backend/pdfs/`
2. **Start Backend**: `uvicorn app.main:app --reload`
3. **Start Frontend**: `npm run dev`
4. **Ask Questions**: Type queries related to PDF content
5. **View Citations**: Click source cards to open PDF viewer
6. **Navigate PDF**: Use zoom controls and page navigation

## Screenshots

### Chat Interface
- Clean, centered layout
- Streaming responses with typing effect
- Tool call indicators showing reasoning
- Numbered citations inline
- Source cards below responses

### PDF Viewer Transition
- Smooth 300ms slide-in animation
- Split-view on desktop (60/40)
- Full-screen on mobile
- Zoom and navigation controls

## Known Limitations

1. **No persistence**: Messages cleared on refresh (add localStorage/DB)
2. **Single user**: No authentication or multi-user support
3. **Mock AI**: Uses template responses (integrate OpenAI/Anthropic API)
4. **Basic search**: Simple text matching (use vector embeddings for semantic search)
5. **No OCR**: Scanned PDFs not supported

## Future Enhancements

- [ ] Vector database (Pinecone/Weaviate) for semantic search
- [ ] Real LLM integration (OpenAI GPT-4, Claude)
- [ ] Redis Queue for production
- [ ] Generative UI components (charts, tables)
- [ ] User authentication
- [ ] Chat history persistence
- [ ] Multi-document comparison
- [ ] Highlight text in PDF viewer

## License

MIT
