import { Component, ElementRef, ViewChild, AfterViewChecked, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, ChatMessage, AgentStep, ApprovalRequest } from '../chat.service';

@Component({
  selector: 'app-chat-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent implements OnInit, AfterViewChecked, OnDestroy {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  isOpen = false;
  isLoading = false;
  isSubmittingApproval = false;
  userInput = '';
  errorMessage: string | null = null;
  abortController: AbortController | null = null;

  messages: ChatMessage[] = [
    {
      id: 'welcome',
      sender: 'assistant',
      text: 'Hello! I am your Library Agent powered by LangGraph, Tool Execution, and Human-in-the-Loop approval. Ask me to search books, check availability, or reserve a book!',
      timestamp: new Date()
    }
  ];

  constructor(public chatService: ChatService) {}

  async ngOnInit(): Promise<void> {
    // Check if there is an existing thread needing recovery on browser refresh
    const savedThreadId = this.chatService.getCurrentThreadId();
    if (savedThreadId) {
      try {
        const state = await this.chatService.getAgentRunState(savedThreadId);
        if (state && (state.is_paused || state.pendingApproval)) {
          const calls = state.state?.pending_calls || state.pending_calls || [];
          this.messages.push({
            id: `recovery_${Date.now()}`,
            sender: 'assistant',
            text: 'Your previous reservation request is pending approval:',
            timestamp: new Date(),
            approvalRequest: {
              threadId: savedThreadId,
              calls: calls.length ? calls : [{ name: 'reserve_book', args: { book_id: 1 } }],
              message: 'Confirmation needed to complete this action.'
            }
          });
        }
      } catch (e) {
        console.warn('Could not restore thread state:', e);
      }
    }
  }

  toggleChat(): void {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.scrollToBottom();
    }
  }

  resetChat(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
    this.chatService.clearThread();
    this.messages = [
      {
        id: 'reset',
        sender: 'assistant',
        text: 'Session and agent thread cleared. Fresh conversation initialized! How can I assist you?',
        timestamp: new Date()
      }
    ];
    this.isLoading = false;
    this.errorMessage = null;
    this.isSubmittingApproval = false;
  }

  async sendMessage(): Promise<void> {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    if (text.length < 3) {
      this.errorMessage = 'Please enter a request with at least 3 characters.';
      return;
    }

    this.errorMessage = null;
    this.userInput = '';

    // Add user message
    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text,
      timestamp: new Date()
    };
    this.messages.push(userMsg);

    // Prepare assistant response entry
    const assistantMsg: ChatMessage = {
      id: `assistant_${Date.now()}`,
      sender: 'assistant',
      text: '',
      timestamp: new Date(),
      isStreaming: true,
      steps: []
    };
    this.messages.push(assistantMsg);

    this.isLoading = true;
    this.abortController = new AbortController();

    try {
      await this.chatService.startAgentRun(
        text,
        {
          onStarted: (threadId: string) => {
            assistantMsg.steps?.push({
              kind: 'thought',
              name: 'router',
              summary: `Started agent execution on thread ${threadId.slice(0, 8)}...`,
              timestamp: new Date()
            });
            this.scrollToBottom();
          },
          onStep: (step: AgentStep) => {
            assistantMsg.steps?.push(step);
            this.scrollToBottom();
          },
          onToken: (token: string) => {
            assistantMsg.text += token;
            this.scrollToBottom();
          },
          onApprovalRequired: (approval: ApprovalRequest) => {
            assistantMsg.isStreaming = false;
            assistantMsg.approvalRequest = approval;
            this.isLoading = false;
            this.scrollToBottom();
          },
          onFinal: (answer: string, sources: string[]) => {
            assistantMsg.isStreaming = false;
            if (!assistantMsg.text) {
              assistantMsg.text = answer;
            }
            this.isLoading = false;
            this.scrollToBottom();
          },
          onError: (err) => {
            this.errorMessage = `${err.message} ${err.retryable ? '(Retryable)' : ''}`;
            assistantMsg.isStreaming = false;
            this.isLoading = false;
            this.scrollToBottom();
          }
        },
        this.abortController.signal
      );
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        this.errorMessage = err.message || 'Failed to complete agent run.';
      }
      assistantMsg.isStreaming = false;
    } finally {
      this.isLoading = false;
      this.abortController = null;
    }
  }

  async handleApproval(msg: ChatMessage, approved: boolean): Promise<void> {
    if (!msg.approvalRequest || this.isSubmittingApproval) return;

    // Double-click protection: disable immediately
    this.isSubmittingApproval = true;
    const threadId = msg.approvalRequest.threadId;

    msg.steps?.push({
      kind: 'tool_call',
      name: 'human_approval',
      summary: approved ? 'User Approved action.' : 'User Rejected action.',
      timestamp: new Date()
    });

    try {
      await this.chatService.resumeAgentRun(
        threadId,
        approved,
        {
          onStep: (step: AgentStep) => {
            msg.steps?.push(step);
            this.scrollToBottom();
          },
          onFinal: (answer: string) => {
            msg.text = (msg.text ? msg.text + '\n' : '') + answer;
            msg.approvalRequest = undefined;
            this.isSubmittingApproval = false;
            this.scrollToBottom();
          },
          onError: (err) => {
            this.errorMessage = `Resume failed: ${err.message}`;
            this.isSubmittingApproval = false;
            this.scrollToBottom();
          }
        }
      );
      msg.approvalRequest = undefined;
    } catch (err: any) {
      this.errorMessage = err.message || 'Failed to resume agent.';
    } finally {
      this.isSubmittingApproval = false;
    }
  }

  async cancelStreaming(): Promise<void> {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
    const threadId = this.chatService.getCurrentThreadId();
    if (threadId) {
      await this.chatService.cancelAgentRun(threadId);
    }
    this.isLoading = false;
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  ngOnDestroy(): void {
    if (this.abortController) {
      this.abortController.abort();
    }
  }

  private scrollToBottom(): void {
    try {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    } catch {}
  }
}
