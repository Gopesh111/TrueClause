# 🛡️ TrueClause
**Enterprise-Grade Contract Intelligence & Negotiation Assistant**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Logic-green)
![Groq](https://img.shields.io/badge/Groq-Llama%203-black)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-orange)

> "I Agree." These two words take 1 second to click, but can trap you in restrictive and asymmetric contracts. TrueClause is built to fix this information asymmetry.

 ## ⚡ The Core Problem & Solution
General AI models suffer from **Alert Fatigue**—they flag *everything* as a risk when analyzing legal documents. 

**TrueClause** is not a basic "Chat with PDF" wrapper. It is a baseline-aware intelligence tool that uses custom rule engines to differentiate between standard industry practices (Green Flags) and actual predatory deviations (Hidden Risks). 

**Key Features:**
- 🕵️‍♂️ **Asymmetric Clause Detection:** Audits Job Offers, Rent Agreements, Freelance Contracts, and NDAs.
- 📊 **Risk Exposure Scoring:** Quantifies risk into a percentage-based, easy-to-understand metric.
- ✍️ **Agentic Negotiation:** Automatically drafts polite, corporate-ready emails to help you negotiate one-sided terms directly.

---

## 🧠 System Architecture (Under the Hood)

This project was engineered with a strict focus on **Fault Tolerance**, **Explainability**, and **Clean Code Architecture**.

### 1. Multi-LLM Failover Orchestration (Zero Downtime)
Cloud services crash and rate limits happen, but production apps shouldn't fail. The system features a built-in active routing mechanism:
- **Primary Inference Engine:** Google Gemini 2.5 Flash.
- **High-Speed Fallback Node:** Groq Llama-3 (70B). If the primary engine hits a rate limit (Error 429) or times out, the payload is instantly and silently rerouted to the backup engine, ensuring a seamless user experience.

### 2. Bulletproof JSONs via Pydantic (Strict Outputs)
LLMs are notorious for hallucinating text and breaking JSON structures. To build a crash-proof UI, the LLM is forced to output strict deterministic schemas using `Pydantic` models (`RiskItem` & `SafeItem`). The AI doesn't just say "this is bad"—it explicitly extracts the quote, states the industry baseline, and highlights the exact deviation.

### 3. Modular Component-Based UI
Moving away from monolithic Streamlit scripts, the frontend is built with a highly scalable, component-based architecture (similar to React). It cleanly isolates the UI components (Sidebar, Dashboard, Analyzers) from the core AI engine.

### 4. Zero-Cost Analytics via Discord Webhooks
Integrated a secure, real-time anonymous feedback loop directly connecting the frontend to a Discord channel via webhooks for seamless beta-testing and bug reporting.

---

## 🛠️ Tech Stack
- **Frontend & UI:** Streamlit (Modularized & White-labeled)
- **AI / LLM Orchestration:** LangChain, Google Generative AI (Gemini), Groq API
- **Data Validation & Parsing:** Pydantic, PyPDF2
- **Language Support:** English, Hindi, Hinglish

---

## 📂 Folder Structure
```text
TrueClause-Analyzer/
├── app.py                     # Master Router & UI Assembly
├── core/
│   └── backend.py             # Brain: Multi-LLM Failover, Prompts, Pydantic Models
├── components/                # Modular UI Elements
│   ├── analyze_ui.py          # PDF Upload & Extraction Logic
│   ├── demo_ui.py             # Instant zero-latency pre-loaded demos
│   ├── dashboard_ui.py        # Dynamic Intelligence Dashboard & Agentic Emailer
│   └── sidebar.py             # Webhook Feedback Form
├── rules/                     # Context-Aware Dictionaries (Employment, Rent, etc.)
└── requirements.txt           # Dependencies
