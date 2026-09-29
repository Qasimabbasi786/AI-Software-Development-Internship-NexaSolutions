# Week 3 - Part G: AI & Python Foundations (Kickoff)

## 📌 Overview
This part introduces hands-on AI scripting using Python. It builds a standalone Python CLI tool using an LLM SDK to generate book summaries and genre recommendations, maintaining key isolation via `.env`.

## 🎯 Technical Concepts
- **AI Core Definitions**: AI vs. Machine Learning vs. Deep Learning vs. NLP vs. Generative AI.
- **Large Language Models (LLM)**: Text prediction engine powering modern LLM APIs.
- **Training vs. Inference**: Pre-computed model weights vs. runtime generation calls.
- **Tokens & Context Window**: Sub-word units measuring API costs and context capacity.
- **Hallucinations**: Why LLMs generate plausible yet false facts when lacking direct grounding.
- **Environment Isolation**: Python `venv` virtual environments & `python-dotenv` key management.

## 📁 Suggested Subfolder Layout
```text
Week_03_PartG_AIScripts/
├── README.md
├── requirements.txt
├── .env.example
└── main.py
```

## 📝 Execution Checklist & Placeholders
- [ ] Create Python virtual environment (`python -m venv .venv`)
- [ ] Install SDK (`google-genai` / `anthropic` / `openai`) & `python-dotenv`
- [ ] Create `.env` for local API keys (verified git-ignored)
- [ ] Write script querying LLM with book title/description to output 1-paragraph summary
- [ ] Experiment with prompt variations (plain question, direct instruction, persona prompt)
