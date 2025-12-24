import { create } from 'zustand';
import { Message, PDFViewerState } from '@/types';

interface ChatStore {
  messages: Message[];
  isStreaming: boolean;
  pdfViewer: PDFViewerState;
  addMessage: (message: Message) => void;
  updateLastMessage: (content: string) => void;
  setStreaming: (streaming: boolean) => void;
  openPDFViewer: (document: string, page: number, citation?: any) => void;
  closePDFViewer: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isStreaming: false,
  pdfViewer: { isOpen: false, document: '', page: 1 },
  
  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),
  
  updateLastMessage: (content) => set((state) => {
    const messages = [...state.messages];
    if (messages.length > 0) {
      messages[messages.length - 1].content += content;
    }
    return { messages };
  }),
  
  setStreaming: (streaming) => set({ isStreaming: streaming }),
  
  openPDFViewer: (document, page, citation) => set({ 
    pdfViewer: { isOpen: true, document, page, citation } 
  }),
  
  closePDFViewer: () => set({ 
    pdfViewer: { isOpen: false, document: '', page: 1 } 
  }),
}));
