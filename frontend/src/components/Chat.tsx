'use client';
import { useEffect, useRef } from 'react';
import { useChatStore } from '@/store/chatStore';
import { sendMessage, streamResponse } from '@/lib/api';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';
import { Message, Citation, Source, ToolCall } from '@/types';

export default function Chat() {
  const { messages, isStreaming, addMessage, setStreaming } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const currentMessageRef = useRef<Message | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (msg: string) => {
    addMessage({ id: Date.now().toString(), role: 'user', content: msg, timestamp: Date.now() });
    setStreaming(true);

    const assistantMsg: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      citations: [],
      sources: [],
      toolCalls: [],
      timestamp: Date.now(),
    };
    currentMessageRef.current = assistantMsg;
    addMessage(assistantMsg);

    try {
      const jobId = await sendMessage(msg);
      
      streamResponse(jobId, (event) => {
        if (!currentMessageRef.current) return;

        const updatedMsg = { ...currentMessageRef.current };

        switch (event.type) {
          case 'text':
            updatedMsg.content += event.content;
            break;
          case 'tool_call':
            updatedMsg.toolCalls = [...(updatedMsg.toolCalls || []), event.data as ToolCall];
            break;
          case 'citation':
            updatedMsg.citations = [...(updatedMsg.citations || []), event.data as Citation];
            break;
          case 'source':
            updatedMsg.sources = [...(updatedMsg.sources || []), event.data as Source];
            break;
          case 'done':
            setStreaming(false);
            currentMessageRef.current = null;
            return;
          case 'error':
            setStreaming(false);
            currentMessageRef.current = null;
            return;
        }

        currentMessageRef.current = updatedMsg;
        useChatStore.setState((state) => ({
          messages: state.messages.map((m) => m.id === updatedMsg.id ? updatedMsg : m)
        }));
      });
    } catch (error) {
      setStreaming(false);
      currentMessageRef.current = null;
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {isStreaming && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <ChatInput onSend={handleSend} disabled={isStreaming} />
    </div>
  );
}
