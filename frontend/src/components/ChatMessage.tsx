'use client';
import { Message } from '@/types';
import { useChatStore } from '@/store/chatStore';

export default function ChatMessage({ message }: { message: Message }) {
  const openPDFViewer = useChatStore((s) => s.openPDFViewer);

  if (message.role === 'user') {
    return (
      <div className="flex justify-end mb-6">
        <div className="bg-blue-600 text-white px-4 py-2 rounded-2xl max-w-2xl">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="mb-8">
      {message.toolCalls && message.toolCalls.length > 0 && (
        <div className="mb-3 space-y-2">
          {message.toolCalls.map((tc, i) => (
            <div key={i} className="text-sm text-gray-500 flex items-center gap-2">
              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse" />
              {tc.status}
            </div>
          ))}
        </div>
      )}
      
      <div className="prose max-w-none text-gray-800">
        {message.content}
      </div>

      {message.sources && message.sources.length > 0 && (
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
          {message.sources.map((src) => (
            <button
              key={src.id}
              onClick={() => openPDFViewer(src.document, src.page)}
              className="text-left p-3 border rounded-lg hover:bg-gray-50 transition"
            >
              <div className="text-xs text-gray-500">Source {src.id}</div>
              <div className="font-medium text-sm">{src.title}</div>
              <div className="text-xs text-gray-400">Page {src.page}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
