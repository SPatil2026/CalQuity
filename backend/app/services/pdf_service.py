import os
from typing import Dict, List, Tuple
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self, pdf_directory: str = "pdfs"):
        self.pdf_directory = pdf_directory
        self.pdf_cache: Dict[str, Dict[int, str]] = {}
        self._load_pdfs()
    
    def _load_pdfs(self):
        """Load and cache all PDFs in the directory"""
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
            return
        
        pdf_count = 0
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                try:
                    self._extract_pdf_text(filename)
                    pdf_count += 1
                    logger.info(f"Loaded PDF: {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
        
        logger.info(f"Total PDFs loaded: {pdf_count}")
    
    def _extract_pdf_text(self, filename: str) -> Dict[int, str]:
        """Extract text from PDF and cache by page"""
        if filename in self.pdf_cache:
            return self.pdf_cache[filename]
        
        filepath = os.path.join(self.pdf_directory, filename)
        reader = PdfReader(filepath)
        
        page_texts = {}
        for page_num, page in enumerate(reader.pages, start=1):
            page_texts[page_num] = page.extract_text()
        
        self.pdf_cache[filename] = page_texts
        return page_texts
    
    def search_documents(self, query: str) -> List[Tuple[str, int, str]]:
        """Search for query in all documents, return (filename, page, excerpt)"""
        results = []
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 2]
        
        logger.info(f"Searching for: '{query}' in {len(self.pdf_cache)} documents")
        
        for filename, pages in self.pdf_cache.items():
            for page_num, text in pages.items():
                text_lower = text.lower()
                
                # Calculate relevance score
                score = 0
                match_positions = []
                
                # Check for exact phrase match (highest score)
                if query_lower in text_lower:
                    score += 100
                    match_positions.append(text_lower.find(query_lower))
                
                # Check for word matches
                for word in query_words:
                    if word in text_lower:
                        score += 10
                        if not match_positions:
                            match_positions.append(text_lower.find(word))
                
                # Only include if there's a match
                if score > 0:
                    # Extract excerpt around best match
                    idx = match_positions[0] if match_positions else 0
                    start = max(0, idx - 100)
                    end = min(len(text), idx + 300)
                    excerpt = text[start:end].strip()
                    
                    if excerpt:
                        results.append((filename, page_num, excerpt, score))
                        logger.info(f"Found match in {filename}, page {page_num}, score: {score}")
        
        # Sort by score (highest first) and return top 5
        results.sort(key=lambda x: x[3], reverse=True)
        logger.info(f"Found {len(results)} results, returning top 5")
        
        return [(f, p, e) for f, p, e, s in results[:5]]
    
    def get_pdf_path(self, filename: str) -> str:
        """Get full path to PDF file"""
        return os.path.join(self.pdf_directory, filename)
    
    def list_documents(self) -> List[str]:
        """List all available PDF documents"""
        return list(self.pdf_cache.keys())
    
    def reload_pdfs(self):
        """Reload all PDFs from directory"""
        logger.info("Reloading PDFs...")
        self.pdf_cache.clear()
        self._load_pdfs()
        return len(self.pdf_cache)

pdf_service = PDFService()
