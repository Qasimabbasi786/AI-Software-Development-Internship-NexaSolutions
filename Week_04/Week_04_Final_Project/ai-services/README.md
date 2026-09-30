# Week 3 - AI Track: Standalone Python LLM Script
### Google Gemini API Integration (`ai-services`)

Welcome to the AI Track module for the **Week 3 Final Project** in the **Nexa Solutions AI Software Development Internship Program**.

This module introduces our first hands-on LLM scripting using **Google Gemini API** (`gemini-flash-latest`) and **Python 3.x**. It takes a book title and description, queries the Gemini model for a concise one-paragraph summary and literary genre suggestions, and outputs the result to the console.

---

## 📌 Architecture & Design Decisions

### Why the AI Script Stays Standalone This Week
Wiring LLM calls directly into the .NET API before prompt engineering, structured outputs, schema verification, and latency/fallback error handling are covered (Week 4) creates architectural instability. Keeping this script standalone proves LLM integration cleanly, while real backend embedding takes place in subsequent weeks.

```
┌────────────────────────────────────────────────────────┐
│             CLI / Standalone Python Script             │
│  - Input: Title & Description arguments                │
│  - Environment: GEMINI_API_KEY loaded via python-dotenv│
└──────────────────────────┬─────────────────────────────┘
                           │ Generative Content Prompt
                           ▼
┌────────────────────────────────────────────────────────┐
│             Google Gemini API                          │
│  - Model: gemini-flash-latest                          │
│  - Generates: 1-paragraph summary & 3 suggested genres │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
                    Console Terminal
```

---

## 📁 Directory Structure

```
ai-services/
├── requirements.txt            # Python dependencies (google-generativeai, python-dotenv, Pillow)
├── summarize_book.py           # Core execution script querying Gemini API
├── .env.example                # Safe environment variable template
├── .env                        # Local secret key file (gitignored)
└── README.md                   # Technical documentation and execution guide
```

---

## 🔒 Configuration & Environment (`.env`)

A dedicated `.env` file is placed inside this directory containing the Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> [!NOTE]
> `.env` is strictly protected by root `.gitignore` to prevent secret credentials from entering source control.

---

## 🚀 Execution Guide

Run the script using our dedicated AI virtual environment:

```bash
# Navigate to ai-services directory
cd Week_03/Week_03_Final_Project/ai-services

# Install dependencies inside the AI environment
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m pip install -r requirements.txt

# Run script with default sample inputs (Faiz Ahmed Faiz poetry collection)
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" summarize_book.py

# Run script with custom book title and description
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" summarize_book.py "Design Patterns" "Elements of Reusable Object-Oriented Software by the Gang of Four."
```
