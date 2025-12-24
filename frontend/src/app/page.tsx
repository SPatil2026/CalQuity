'use client';
import Chat from '@/components/Chat';
import PDFViewer from '@/components/PDFViewer';
import { useChatStore } from '@/store/chatStore';

export default function Home() {
  const pdfViewer = useChatStore((s) => s.pdfViewer);

  return (
    <main className="h-screen flex flex-col md:flex-row">
      <div className={`flex-1 flex flex-col ${pdfViewer.isOpen ? 'hidden md:flex md:w-3/5' : 'w-full'}`}>
        <header className="border-b p-4 bg-white">
          <h1 className="text-xl font-semibold text-center">AI Search Chat</h1>
        </header>
        <Chat />
      </div>
      <PDFViewer />
    </main>
  );
}
