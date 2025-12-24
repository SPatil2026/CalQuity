# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Add Sample PDF (Optional)
```bash
# Install reportlab for PDF generation
pip install reportlab

# Generate sample PDF
python generate_sample_pdf.py
```

Or manually add your own PDF files to `backend/pdfs/` directory.

### Step 3: Start Backend
```bash
uvicorn app.main:app --reload
```
✅ Backend running at http://localhost:8000

### Step 4: Frontend Setup
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
✅ Frontend running at http://localhost:3000

### Step 5: Test the Application
1. Open http://localhost:3000 in your browser
2. Type a question related to your PDF content
3. Watch the streaming response with tool calls
4. Click on source cards to open the PDF viewer

## 🎯 Example Queries

If using the sample PDF:
- "What is artificial intelligence?"
- "Tell me about machine learning"
- "What are applications of AI?"

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.11+)
- Ensure virtual environment is activated
- Check port 8000 is not in use

**Frontend won't start:**
- Check Node version: `node --version` (need 20+)
- Delete `node_modules` and run `npm install` again
- Check port 3000 is not in use

**No PDFs found:**
- Add PDF files to `backend/pdfs/` directory
- Restart backend server to reload PDFs

**CORS errors:**
- Ensure backend is running on port 8000
- Check frontend .env.local has correct API URL

## 📦 Docker Alternative

```bash
# From project root
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
