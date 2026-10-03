# Library Management Client (Angular 18+ Reactive UI & Streaming AI Assistant)
### Week 6 Final Project — Frontend Application (`libraryFrontend`)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 Final Project — Real-Time SSE Token-by-Token Streaming Client  

[![Angular: 18](https://img.shields.io/badge/Angular-18_Standalone-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4%2B-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Streaming: SSE](https://img.shields.io/badge/Streaming-Server--Sent_Events-FF5722)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 🎨 UI/UX Features & Design Philosophy

1. **Modern Standalone Architecture**: Built with Angular 18 standalone components, signals, and typed reactive forms.
2. **Real-Time Token-by-Token Streaming**: Integrates a responsive, floating AI Assistant drawer that renders live LLM tokens progressively as they are emitted from the server.
3. **Native Fetch & ReadableStream Integration**: Uses native browser `fetch` and `ReadableStream.getReader()` to parse Server-Sent Events (`data: ...`), overcoming `HttpClient` buffer constraints.
4. **Session Memory & Abort Controls**: Allows users to start fresh conversation sessions and cancel mid-stream generation on demand using `AbortController`.
5. **Robust State & Error Handling**: Gracefully handles network disconnects and circuit breaker states with informative UI alerts.

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 Angular SPA (Port 4200)                     │
│                                                             │
│  ┌────────────────────────┐      ┌───────────────────────┐  │
│  │   BookListComponent    │      │ ChatAssistantComponent│  │
│  │  - Table Roster & Cards│      │  - Floating AI drawer │  │
│  │  - Loading/Error states│      │  - Token stream render│  │
│  └───────────┬────────────┘      └───────────┬───────────┘  │
│              │                               │              │
│              ▼                               ▼              │
│     BookService (RxJS)               ChatService (Fetch)    │
│     - CRUD via HttpClient            - SSE ReadableStream   │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               └───────────────┬───────────────┘
                               ▼
            ASP.NET Core Web API Gateway (Port 5000)
                               │
                               ▼
            FastAPI AI Microservice (Port 8000)
```

---

## 📁 Directory Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── chat-assistant/
│   │   │   ├── chat-assistant.component.ts     # Standalone streaming chat component
│   │   │   ├── chat-assistant.component.html   # Floating drawer layout with live cursor
│   │   │   └── chat-assistant.component.css    # Modern glassmorphism & responsive styles
│   │   ├── chat.service.ts                     # Native fetch SSE reader & session service
│   │   ├── book-form/                          # Book creation & editing reactive forms
│   │   ├── book-list/                          # Catalog list & availability badges
│   │   ├── auth.service.ts                     # JWT authentication state management
│   │   ├── app.component.ts                    # Root component hosting layout and chat
│   │   └── app.routes.ts                       # Angular SPA routing definitions
│   ├── environments/                           # Dynamic API URLs (development & prod)
│   └── styles.css                              # Global CSS design tokens
└── package.json                                # Angular dependencies
```

---

## 🚀 Execution Guide

```powershell
# 1. Navigate to frontend directory
cd "Week_06/Week_06_Final_Project/frontend"

# 2. Run the Angular development server
npm start
```
- **App Access:** `http://localhost:4200`
- Click the floating **🤖 Ask AI Assistant** button at the bottom-right corner to initiate live streaming conversations.
