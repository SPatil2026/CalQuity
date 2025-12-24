import asyncio
import os
from typing import AsyncGenerator, Dict
from app.services.pdf_service import pdf_service
from google import genai
from google.genai import types
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        logger.info(f"Checking API key: {api_key[:10] if api_key else 'None'}...")
        
        if api_key and api_key != "your_gemini_api_key_here" and len(api_key) > 20:
            self.client = genai.Client(api_key=api_key)
            self.use_real_ai = True
            logger.info("✅ Gemini AI enabled")
        else:
            self.use_real_ai = False
            logger.warning("⚠️ Gemini API key not set, using mock responses")
    
    async def generate_response(self, message: str) -> AsyncGenerator[Dict, None]:
        """Generate AI response with streaming, tool calls, and citations"""
        
        # Tool call: Thinking
        yield {"type": "tool_call", "data": {"tool": "thinking", "status": "Analyzing your question..."}}
        await asyncio.sleep(0.5)
        
        # Tool call: Searching documents
        yield {"type": "tool_call", "data": {"tool": "searching_documents", "status": "🔍 Searching documents..."}}
        await asyncio.sleep(0.8)
        
        # Search for relevant documents
        search_results = pdf_service.search_documents(message)
        
        # Tool call: Retrieving PDFs
        yield {"type": "tool_call", "data": {"tool": "retrieving_pdf", "status": "📄 Reading PDF sections..."}}
        await asyncio.sleep(0.6)
        
        # Tool call: Analyzing content
        yield {"type": "tool_call", "data": {"tool": "analyzing_content", "status": "🤔 Analyzing content..."}}
        await asyncio.sleep(0.7)
        
        # Yield citations first
        for idx, (doc, page, excerpt) in enumerate(search_results, 1):
            yield {
                "type": "citation",
                "data": {"id": idx, "document": doc, "page": page, "text": excerpt}
            }
        
        # Generate response
        if search_results:
            if self.use_real_ai:
                async for event in self._generate_with_gemini(message, search_results):
                    yield event
            else:
                async for event in self._generate_mock(message, search_results):
                    yield event
            
            # Yield sources
            for idx, (doc, page, excerpt) in enumerate(search_results, 1):
                yield {
                    "type": "source",
                    "data": {
                        "id": idx,
                        "title": doc.replace('.pdf', '').replace('_', ' ').title(),
                        "document": doc,
                        "page": page
                    }
                }
        else:
            response = "I couldn't find specific information about that in the available documents. Could you rephrase your question or ask about something else?"
            for word in response.split():
                yield {"type": "text", "content": word + " "}
                await asyncio.sleep(0.03)
        
        yield {"type": "done"}
    
    async def _generate_with_gemini(self, message: str, search_results) -> AsyncGenerator[Dict, None]:
        """Generate response using Gemini API"""
        context = "\n\n".join([
            f"[Source {idx}] From {doc} (page {page}):\n{excerpt}"
            for idx, (doc, page, excerpt) in enumerate(search_results, 1)
        ])
        
        prompt = f"""Based on the following document excerpts, answer the user's question. 
Include citation numbers [1], [2], etc. when referencing sources.

Context:
{context}

Question: {message}

Answer:"""
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            if response.text:
                for word in response.text.split():
                    yield {"type": "text", "content": word + " "}
                    await asyncio.sleep(0.03)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            async for event in self._generate_mock(message, search_results):
                yield event
    
    async def _generate_mock(self, message: str, search_results) -> AsyncGenerator[Dict, None]:
        """Generate mock response (fallback)"""
        first_doc, first_page, first_excerpt = search_results[0]
        
        response_parts = [
            f"Based on the documents, I found relevant information:\n\n",
            f"According to {first_doc.replace('.pdf', '').replace('_', ' ')} (page {first_page}) [1], ",
            f'"{first_excerpt[:300] if len(first_excerpt) > 300 else first_excerpt}"'
        ]
        
        if len(search_results) > 1:
            other_sources = ', '.join(str(i) for i in range(2, min(len(search_results)+1, 6)))
            response_parts.append(f"\n\nAdditional relevant information can be found in sources [{other_sources}].")
        
        full_response = "".join(response_parts)
        for word in full_response.split():
            yield {"type": "text", "content": word + " "}
            await asyncio.sleep(0.03)

ai_service = AIService()
