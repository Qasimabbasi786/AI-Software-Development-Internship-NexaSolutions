# Week 4 - Part D: LLM APIs In Depth (Google Gemini)

## 📌 Executive Summary
In Week 4 - Part D, we transition from simple one-line model prompts to mastering production-grade **LLM API mechanics** using the **Google Gemini API (`gemini-3.8-flash`)** inside our dedicated Python virtual environment (`AI_env`).

This module implements four modular scripts covering:
1. **Hyperparameter Tuning (`temperature`, `max_output_tokens`)**: Comparing deterministic outputs versus varied lexical creativity, and setting token budget guardrails.
2. **Conversational Memory & State Management**: Overcoming the stateless nature of LLMs by preserving and passing conversation turn histories back to the API.
3. **Real-Time Token Streaming**: Measuring Time-to-First-Token (TTFT) and rendering tokens progressively for enhanced user experience.
4. **Structured JSON Output & Defensive Parsing**: Enforcing structured JSON responses and implementing resilient `try/except` fallbacks using `json.loads` and regex pattern extraction.

---

## 🏗️ Core Concepts & Implementation Modules

```
Week_04_PartD_LLMAPIs/
├── .env.example                 # Configuration template for GEMINI_API_KEY
├── .env                         # Local secret key file (git-ignored)
├── requirements.txt             # Dependencies: google-generativeai, python-dotenv, pydantic
├── 01_model_parameters.py       # Experiment 1: Temperature & token budget controls
├── 02_conversation_history.py   # Experiment 2: Multi-turn chat session memory
├── 03_streaming.py              # Experiment 3: Server-side token streaming & TTFT metrics
├── 04_structured_output.py      # Experiment 4: Schema-enforced JSON & defensive parsing
└── README.md                    # Module documentation & execution guide
```

---

## 🔬 In-Depth Concepts Mastered

### 1. Temperature & Token Limits (`01_model_parameters.py`)
- **What `temperature` controls:** Governs the probability distribution when selecting subsequent tokens.
  - `temperature = 0.0`: The model consistently picks the highest-probability token (greedy search). Yields deterministic, factual, and reproducible outputs ideal for classification, code analysis, and structured extraction.
  - `temperature = 1.0`: Flattens the probability curve, introducing lexical diversity and stylistic variation suitable for creative writing and brainstorming.
- **What `max_output_tokens` controls:** Sets a hard upper limit on generated response length, preventing runaway token consumption and runaway API costs.

### 2. Conversational Memory (`02_conversation_history.py`)
- **Stateless LLM Nature:** LLM endpoints have zero server-side memory between HTTP requests. Every call is completely independent.
- **Context Preservation:** To maintain multi-turn context (e.g., remembering a user's favorite book mentioned in Turn 1 during a Turn 2 recommendation query), the entire message history array must be resent:
```python
chat = model.start_chat(history=[])
response1 = chat.send_message("My favorite book is The Pragmatic Programmer.")
# In Turn 2, the chat session includes Turn 1 prompt & response in the request payload
response2 = chat.send_message("Recommend 2 more books like that.")
```

### 3. Server-Side Token Streaming (`03_streaming.py`)
- **Perceived Latency & UX:** Rather than waiting several seconds for a model to finish generating its entire response before displaying anything, streaming returns text chunks progressively.
- **Metric Measured:**
  - **Time-to-First-Token (TTFT):** How fast the user sees initial feedback on screen (typically < 0.5s with Gemini Flash).
```python
response = model.generate_content(prompt, stream=True)
for chunk in response:
    print(chunk.text, end="", flush=True)
```

### 4. Structured JSON Output & Defensive Parsing (`04_structured_output.py`)
- **The Problem:** LLMs can prepend pleasantries or wrap JSON inside markdown blocks (e.g., ` ```json ... ``` `). If your backend assumes the output is raw JSON, calling `json.loads` will crash with a `JSONDecodeError`.
- **Defensive Parser Pipeline:**
  1. Strip markdown delimiters (````json` and ````).
  2. Attempt `json.loads(cleaned)`.
  3. If invalid, run regex extraction: `re.search(r'(\{[\s\S]*\})', raw_output)`.
  4. Gracefully handle errors with safe fallbacks instead of crashing application servers.

---

## 🚀 Execution & Verification Guide

Always execute with the dedicated virtual environment interpreter:

```powershell
cd "Week_04/Week_04_PartD_LLMAPIs"

# 1. Run Model Parameters & Temperature Experiment
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" 01_model_parameters.py

# 2. Run Multi-turn Conversation Memory Demo
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" 02_conversation_history.py

# 3. Run Real-Time Token Streaming Demo
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" 03_streaming.py

# 4. Run Structured JSON Extraction & Resilient Parser
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" 04_structured_output.py
```

---

## 🌿 Git Checkpoint
```bash
git checkout -b feature/llm-apis-depth
git add .
git commit -m "feat: add conversation history, streaming, and structured JSON output examples"
```
