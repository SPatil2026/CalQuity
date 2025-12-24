const API_BASE = 'http://localhost:8000';

export async function sendMessage(message: string): Promise<string> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  return data.job_id;
}

export function streamResponse(jobId: string, onEvent: (event: any) => void) {
  const eventSource = new EventSource(`${API_BASE}/api/chat/stream/${jobId}`);
  
  eventSource.onmessage = (e) => {
    const event = JSON.parse(e.data);
    onEvent(event);
    if (event.type === 'done' || event.type === 'error') {
      eventSource.close();
    }
  };
  
  eventSource.onerror = () => eventSource.close();
  return eventSource;
}

export function getPDFUrl(filename: string): string {
  return `${API_BASE}/api/pdf/${filename}`;
}
