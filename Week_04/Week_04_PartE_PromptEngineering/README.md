# Week 4 - Part E: Prompt Engineering

## 🎯 Objectives
- Understand the distinction between **System Prompts** (role & behavioral guardrails) and **User Prompts** (data / task request).
- Compare **Zero-Shot**, **Few-Shot**, and **Role-Based** prompting strategies for consistency, format adherence, and quality.
- Mitigate **Prompt Injection** attacks by treating untrusted user input strictly as inert data rather than executable instructions.
- Centralize production prompt templates in `prompt_templates.py` for direct import by the FastAPI service.

## 📂 Included Scripts
- `prompt_templates.py`: Centralized system prompt and few-shot templates.
- `prompt_comparison.py`: Demonstration script comparing prompting styles and adversarial prompt injection safety.

## 🌿 Git Checkpoint
```bash
git commit -m "feat: finalize prompt template for genre/summary endpoint"
```
