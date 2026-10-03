import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { AuthService } from './auth.service';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: Date;
  isStreaming?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private sessionId = `session_${Date.now()}`;

  constructor(private auth: AuthService) {}

  getSessionId(): string {
    return this.sessionId;
  }

  resetSession(): void {
    this.sessionId = `session_${Date.now()}`;
  }

  /**
   * Consumes live SSE stream from .NET API proxy (/api/assistant/ask/stream).
   * Uses native fetch and ReadableStream reader to achieve progressive token rendering.
   */
  async askStream(
    question: string,
    onChunk: (token: string) => void,
    abortSignal?: AbortSignal
  ): Promise<void> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };

    const token = this.auth.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${environment.apiUrl}/assistant/ask/stream`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        question,
        sessionId: this.sessionId
      }),
      signal: abortSignal
    });

    if (!response.ok || !response.body) {
      throw new Error(`Streaming request failed with status: ${response.status} ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || ''; // Keep trailing partial chunk in buffer

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data:')) continue;

        const dataContent = trimmed.substring(5).trim();
        if (dataContent === '[DONE]') {
          return;
        }

        onChunk(dataContent);
      }
    }
  }
}
