export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  sources?: Source[];
  toolCalls?: ToolCall[];
  timestamp: number;
}

export interface Citation {
  id: number;
  document: string;
  page: number;
  text: string;
}

export interface Source {
  id: number;
  title: string;
  document: string;
  page: number;
}

export interface ToolCall {
  tool: string;
  status: string;
}

export interface StreamEvent {
  type: 'text' | 'tool_call' | 'citation' | 'source' | 'component' | 'done' | 'error';
  content?: string;
  data?: Record<string, unknown>;
}

export interface PDFViewerState {
  isOpen: boolean;
  document: string;
  page: number;
  citation?: Citation;
}
