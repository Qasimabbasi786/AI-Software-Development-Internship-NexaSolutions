import { Component, ElementRef, ViewChild, AfterViewChecked, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, ChatMessage } from '../chat.service';

@Component({
  selector: 'app-chat-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent implements AfterViewChecked, OnDestroy {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  isOpen = false;
  isLoading = false;
  userInput = '';
  errorMessage: string | null = null;
  abortController: AbortController | null = null;

  messages: ChatMessage[] = [
    {
      id: 'welcome',
      sender: 'assistant',
      text: 'Hello! I am your Library AI Assistant powered by LangChain & Gemini. Ask me about books in our catalog, recommendations, or borrowing availability!',
      timestamp: new Date()
    }
  ];

  constructor(public chatService: ChatService) {}

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
    this.chatService.resetSession();
    this.messages = [
      {
        id: 'reset',
        sender: 'assistant',
        text: 'Session cleared. Fresh conversation initialized! How can I assist you?',
        timestamp: new Date()
      }
    ];
    this.isLoading = false;
    this.errorMessage = null;
  }

  async sendMessage(): Promise<void> {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    if (text.length < 3) {
      this.errorMessage = 'Please enter a question with at least 3 characters.';
      return;
    }

    this.errorMessage = null;
    this.userInput = '';

    // Add user message to history
    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text,
      timestamp: new Date()
    };
    this.messages.push(userMsg);

    // Prepare placeholder assistant message for live token append
    const assistantMsg: ChatMessage = {
      id: `assistant_${Date.now()}`,
      sender: 'assistant',
      text: '',
      timestamp: new Date(),
      isStreaming: true
    };
    this.messages.push(assistantMsg);

    this.isLoading = true;
    this.abortController = new AbortController();

    try {
      await this.chatService.askStream(
        text,
        (chunk: string) => {
          assistantMsg.text += (assistantMsg.text ? ' ' : '') + chunk;
          this.scrollToBottom();
        },
        this.abortController.signal
      );
    } catch (err: any) {
      if (err.name === 'AbortError') {
        assistantMsg.text += ' [Stream cancelled]';
      } else {
        this.errorMessage = 'The AI assistant is temporarily unavailable. Please try again shortly.';
        if (!assistantMsg.text) {
          assistantMsg.text = '⚠️ Service temporarily unavailable. Please check backend connection or retry in a few moments.';
        }
      }
    } finally {
      assistantMsg.isStreaming = false;
      this.isLoading = false;
      this.abortController = null;
      this.scrollToBottom();
    }
  }

  cancelStreaming(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
      this.isLoading = false;
    }
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  private scrollToBottom(): void {
    try {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    } catch {}
  }

  ngOnDestroy(): void {
    if (this.abortController) {
      this.abortController.abort();
    }
  }
}
