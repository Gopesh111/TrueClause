# 🚩 RedFlag.ai
**Enterprise-Grade Contract Risk Analyzer & Negotiation Assistant**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Logic-green)
![Groq](https://img.shields.io/badge/Groq-Llama%203-black)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-orange)

> "I Agree." These two words take 1 second to click, but can trap you in predatory contracts. RedFlag.ai is built to fix this information asymmetry.

🔗 **[Live Application Link]** *(https://redflag-ai-yuj9psj4kzktvshqwnwcru.streamlit.app/)* 
🎬 **[Watch the Demo Video]** *(https://drive.google.com/file/d/1oW73Wb_tIv_dEzhVSzSckd5jS99-kX9R/view?usp=sharing)* 

## ⚡ The Core Problem & Solution
General AI models suffer from **Alert Fatigue**—they flag *everything* as a risk when analyzing legal documents. 

**RedFlag.ai** is not a basic "Chat with PDF" wrapper. It is a baseline-aware risk intelligence tool that uses custom rule engines to differentiate between standard industry practices (Green Flags) and actual predatory deviations (Red Flags). 

**Key Features:**
- 🕵️‍♂️ **Toxic Clause Detection:** Audits Job Offers, Rent Agreements, Freelance Contracts, and NDAs.
- 📊 **Toxicity Scoring:** Quantifies risk into a percentage-based score.
- ✍️ **Agentic Email Generation:** Automatically drafts polite, corporate-ready emails to help you negotiate one-sided terms.

---

## 🧠 System Architecture (Under the Hood)

This project was engineered with a focus on **Fault Tolerance**, **Explainability**, and **Clean Code Architecture**.

### 1. Multi-LLM Failover Engine (100% Uptime)
APIs crash, but production apps shouldn't. The system features a built-in `try-except` failover routing mechanism:
- **Primary Engine:** Google Gemini 2.5 Flash.
- **High-Speed Fallback:** Groq Llama-3 (70B). If the primary engine hits a rate limit (Error 429) or timeouts, the payload is silently and instantly rerouted to the Llama-3 backup engine, ensuring a seamless user experience.

### 2. Taming AI with Pydantic (Structured Outputs)
Raw LLMs hallucinate text. To build a reliable UI, the LLM is forced to output strict `JSON` schemas using Pydantic models (`RiskItem` & `SafeItem`). The AI doesn't just say "this is bad"—it explicitly extracts the quote, states the industry baseline, and highlights the exact deviation.

### 3. Modular Component-Based UI
Built like a modern React/Node app, the monolithic Streamlit script was refactored into a highly scalable, component-based architecture isolating the UI components (Sidebar, Dashboard, Analyzers) from the core AI engine.

### 4. Zero-Cost Analytics via Discord Webhooks
Integrated a secure, real-time anonymous feedback loop directly connecting the frontend to a Discord channel via webhooks for seamless beta-testing and bug reporting.

---

## 🛠️ Tech Stack
- **Frontend & UI:** Streamlit (Modularized)
- **AI / LLM Orchestration:** LangChain, Google Generative AI (Gemini), Groq API
- **Data Validation & Parsing:** Pydantic, PyPDF2
- **Language Support:** English, Hindi, Hinglish

---

## 📂 Folder Structure
```text
RedFlag-AI/
├── app.py                     # Master Router & UI Assembly
├── core/
│   └── backend.py             # Brain: Multi-LLM Failover, Prompts, Pydantic Models
├── components/                # Modular UI Elements
│   ├── analyze_ui.py          # PDF Upload & Extraction Logic
│   ├── demo_ui.py             # Instant zero-latency pre-loaded demos
│   ├── dashboard_ui.py        # Dynamic Toxicity Dashboard & Agentic Emailer
│   └── sidebar.py             # Webhook Feedback Form
├── rules/                     # Context-Aware Dictionaries (Employment, Rent, etc.)
└── requirements.txt           # Dependencies
