import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { AuthService } from './auth.service';

export interface AgentStep {
  kind: 'tool_call' | 'tool_result' | 'thought';
  name: string;
  summary: string;
  timestamp: Date;
}

export interface ApprovalRequest {
  threadId: string;
  calls: Array<{ name: string; args: any }>;
  message: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: Date;
  isStreaming?: boolean;
  steps?: AgentStep[];
  approvalRequest?: ApprovalRequest;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private currentThreadId: string | null = null;

  constructor(private auth: AuthService) {
    // Restore any existing thread id from local storage
    this.currentThreadId = localStorage.getItem('library_agent_thread_id');
  }

  getCurrentThreadId(): string | null {
    return this.currentThreadId;
  }

  setCurrentThreadId(id: string): void {
    this.currentThreadId = id;
    localStorage.setItem('library_agent_thread_id', id);
  }

  clearThread(): void {
    this.currentThreadId = null;
    localStorage.removeItem('library_agent_thread_id');
  }

  /**
   * Starts a typed SSE agent run via .NET API (/api/assistant/agent/runs).
   */
  async startAgentRun(
    question: string,
    callbacks: {
      onStarted?: (threadId: string) => void;
      onStep?: (step: AgentStep) => void;
      onToken?: (token: string) => void;
      onApprovalRequired?: (approval: ApprovalRequest) => void;
      onFinal?: (answer: string, sources: string[]) => void;
      onError?: (error: { code: number; message: string; retryable: boolean }) => void;
    },
    abortSignal?: AbortSignal
  ): Promise<void> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };

    const token = this.auth.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${environment.apiUrl}/assistant/agent/runs`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        question,
        threadId: this.currentThreadId
      }),
      signal: abortSignal
    });

    if (response.status === 429) {
      if (callbacks.onError) {
        callbacks.onError({
          code: 429,
          message: 'Rate limit exceeded: You have made too many agent requests. Please wait a moment.',
          retryable: true
        });
      }
      return;
    }

    if (!response.ok || !response.body) {
      throw new Error(`Agent run failed with status: ${response.status} ${response.statusText}`);
    }

    await this.processSseStream(response.body, callbacks);
  }

  /**
   * Resumes a paused agent run after user approval or rejection.
   */
  async resumeAgentRun(
    threadId: string,
    approved: boolean,
    callbacks: {
      onStep?: (step: AgentStep) => void;
      onFinal?: (answer: string, sources: string[]) => void;
      onError?: (error: { code: number; message: string; retryable: boolean }) => void;
    }
  ): Promise<void> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };

    const token = this.auth.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${environment.apiUrl}/assistant/agent/runs/${threadId}/resume`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ approved })
    });

    if (!response.ok || !response.body) {
      throw new Error(`Resume failed with status: ${response.status} ${response.statusText}`);
    }

    await this.processSseStream(response.body, callbacks);
  }

  /**
   * Retrieves state for page refresh state restoration.
   */
  async getAgentRunState(threadId: string): Promise<any> {
    const headers: Record<string, string> = {};
    const token = this.auth.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${environment.apiUrl}/assistant/agent/runs/${threadId}`, {
      method: 'GET',
      headers
    });

    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error(`Failed to load thread state: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Cancels an ongoing agent run upstream.
   */
  async cancelAgentRun(threadId: string): Promise<void> {
    const headers: Record<string, string> = {};
    const token = this.auth.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    await fetch(`${environment.apiUrl}/assistant/agent/runs/${threadId}/cancel`, {
      method: 'POST',
      headers
    });
  }

  /**
   * Parses Server-Sent Events stream dispatching typed callbacks.
   */
  private async processSseStream(
    body: ReadableStream<Uint8Array>,
    callbacks: any
  ): Promise<void> {
    const reader = body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data:')) continue;

        const dataContent = trimmed.substring(5).trim();
        if (dataContent === '[DONE]') return;

        try {
          const payload = JSON.parse(dataContent);
          const evtType = payload.event;

          if (evtType === 'started' && callbacks.onStarted) {
            this.setCurrentThreadId(payload.threadId);
            callbacks.onStarted(payload.threadId);
          } else if (evtType === 'step' && callbacks.onStep) {
            callbacks.onStep({
              kind: payload.kind || 'tool_call',
              name: payload.name || 'tool',
              summary: payload.summary || '',
              timestamp: new Date()
            });
          } else if (evtType === 'token' && callbacks.onToken) {
            callbacks.onToken(payload.text);
          } else if (evtType === 'approval_required' && callbacks.onApprovalRequired) {
            callbacks.onApprovalRequired({
              threadId: payload.threadId,
              calls: payload.calls || [],
              message: payload.message || 'Action requires user confirmation.'
            });
          } else if (evtType === 'final' && callbacks.onFinal) {
            callbacks.onFinal(payload.answer, payload.sources || []);
          } else if (evtType === 'error' && callbacks.onError) {
            callbacks.onError({
              code: payload.code || 500,
              message: payload.message || 'Error executing agent task.',
              retryable: !!payload.retryable
            });
          }
        } catch {
          // If non-JSON chunk, treat as raw text token for compatibility
          if (callbacks.onToken) {
            callbacks.onToken(dataContent);
          }
        }
      }
    }
  }

  /**
   * Backward-compatible askStream for legacy components.
   */
  async askStream(
    question: string,
    onChunk: (token: string) => void,
    abortSignal?: AbortSignal
  ): Promise<void> {
    await this.startAgentRun(
      question,
      {
        onToken: onChunk,
        onFinal: (answer) => onChunk('\n' + answer)
      },
      abortSignal
    );
  }
}
