# Week 3 - Part G: AI & Python Foundations (Kickoff)

## 📌 Overview
This module introduces the first hands-on AI scripting component of the internship using **Python 3.x** and the **Anthropic SDK** (`anthropic`). 

It establishes clean environment isolation via `python-dotenv`, explores fundamental Large Language Model (LLM) concepts, documents prompt engineering variations, and analyzes LLM hallucinations on fictional queries.

---

## 🧠 Core Technical Concepts & Definitions

1. **AI / ML / Deep Learning / NLP / Generative AI Hierarchy**:
   - **Artificial Intelligence (AI)**: Broader science of creating intelligent systems.
   - **Machine Learning (ML)**: Subfield of AI where algorithms learn patterns from data.
   - **Deep Learning (DL)**: Subset of ML using deep multi-layered neural networks.
   - **Natural Language Processing (NLP)**: Domain focusing on understanding human language text and speech.
   - **Generative AI**: Class of AI models capable of generating new text, images, or audio content.

2. **LLM (Large Language Model)**:
   - A neural network trained on vast text corpora to predict the most statistically probable next token in a sequence.

3. **Training vs. Inference**:
   - **Training**: Massive, resource-intensive process where provider pre-computes model weights on training data.
   - **Inference**: Runtime execution when a prompt is sent to the API and the model generates a response.

4. **Tokens & Context Window**:
   - **Token**: Basic unit of text processed by an LLM (roughly 3/4 of a word in English). API billing is measured in tokens.
   - **Context Window**: Maximum number of combined input (prompt) and output (response) tokens the model can process in a single request.

5. **Hallucination**:
   - Occurs when an LLM confidently outputs plausible-sounding yet false or ungrounded facts because it predicts text probabilities rather than querying a verified truth database.

---

## 🧪 Experiments & Prompt Analysis

### Experiment 1: Prompt Variations

| Prompt Strategy | Input Prompt | Observed Output Characteristics |
| :--- | :--- | :--- |
| **Plain Question** | *"Who was Faiz Ahmed Faiz and what is his legacy?"* | Descriptive, conversational, multi-paragraph background narrative. |
| **Direct Instruction** | *"Summarize the core themes in exactly 3 bullet points."* | Structured, concise, strictly formatted output adhering to bullet constraints. |
| **Persona Role Prompt** | *"You are a strict librarian..."* + *"What books are available?"* | Formal tone, restricted brevity, adhering strictly to system role constraints. |

---

### Experiment 2: Hallucination Test

- **Test Query**: *"Provide a detailed summary of the 1994 Islamabad Cybernetic Quantum Computer Conference organized by Professor Tariq Hashmi."*
- **Observation & Result**: 
  - Without external retrieval grounding (RAG), LLMs may attempt to synthesize plausible details about quantum computing in Islamabad.
  - **Mitigation Strategy**: Real integration (Week 6) will ground LLM responses by injecting retrieved database context from PostgreSQL into the prompt.

---

## 🚀 Execution Instructions

1. **Set Up Python Virtual Environment**:
   ```bash
   python -m venv .venv
   
   # Windows PowerShell
   .venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Local Environment Key**:
   - Create a local `.env` file (verified `.gitignore` protected).
   - Add your API key:
     ```env
     ANTHROPIC_API_KEY=your_actual_api_key_here
     ```
4. **Run Script**:
   ```bash
   python main.py
   ```

---

## 📢 Git Checkpoint
```bash
git add Week_03_PartG_AIScripts/
git commit -m "feat: add first AI Python script with dotenv key loading and prompt experiments"
```
