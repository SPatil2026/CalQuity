'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '@/store/chatStore';
import { getPDFUrl } from '@/lib/api';
import { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export default function PDFViewer() {
  const { pdfViewer, closePDFViewer } = useChatStore();
  const [numPages, setNumPages] = useState<number>(0);
  const [scale, setScale] = useState(1.0);

  if (!pdfViewer.isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ x: '100%', opacity: 0, scale: 0.95 }}
        animate={{ x: 0, opacity: 1, scale: 1 }}
        exit={{ x: '100%', opacity: 0, scale: 0.95 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        className="fixed md:relative top-0 right-0 h-full w-full md:w-2/5 bg-white border-l shadow-2xl z-50 flex flex-col"
      >
        <div className="flex items-center justify-between p-4 border-b bg-gray-50">
          <div className="text-sm font-medium">
            {pdfViewer.document.replace('.pdf', '')} - Page {pdfViewer.page}/{numPages}
          </div>
          <div className="flex gap-2">
            <button onClick={() => setScale(s => Math.max(0.5, s - 0.2))} className="px-3 py-1 border rounded hover:bg-gray-100">-</button>
            <button onClick={() => setScale(s => Math.min(2, s + 0.2))} className="px-3 py-1 border rounded hover:bg-gray-100">+</button>
            <button onClick={closePDFViewer} className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300">✕</button>
          </div>
        </div>
        <div className="flex-1 overflow-auto bg-gray-100 flex justify-center p-4">
          <Document
            file={getPDFUrl(pdfViewer.document)}
            onLoadSuccess={({ numPages }) => setNumPages(numPages)}
            loading={<div className="text-gray-500">Loading PDF...</div>}
            error={<div className="text-red-500">Failed to load PDF</div>}
          >
            <Page pageNumber={pdfViewer.page} scale={scale} />
          </Document>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
