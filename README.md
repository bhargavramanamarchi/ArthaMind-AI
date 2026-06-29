---
title: ArthaMind AI
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.12.0
app_file: app.py
pinned: true
license: mit
---

<div align="center">

# 🧠 ArthaMind AI

### *Your Intelligent Personal Finance Advisor for Indian Citizens*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-5.0+-FF6F00?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**ArthaMind AI** is a production-grade, multilingual AI-powered personal finance assistant built for Indian citizens. It combines Large Language Models, Retrieval Augmented Generation, Voice AI, and Smart Financial Calculators in a beautiful dark-themed UI.

*"Artha" (अर्थ) means wealth in Sanskrit — ArthaMind is the AI mind for your wealth.*

---

# 🚀 Live Demo

### 🌐 Try ArthaMind AI Online

**🔗 Hugging Face Deployment**

https://huggingface.co/spaces/Bhargav-06/ArthaMind-Personal-Finance-Advisor

**💻 GitHub Repository**

https://github.com/bhargavramanamarchi/ArthaMind-AI

---

### 📌 Quick Navigation

**🚀 Live Demo** • **✨ Features** • **⚙️ Installation** • **🏗️ Architecture** • **📸 Screenshots**

---

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat Assistant** | Context-aware financial Q&A powered by Gemini 2.5 Flash with RAG |
| 🎙️ **Voice Assistant** | Speak in Hindi, Telugu, Tamil, Kannada, or Malayalam — get voice responses |
| 📈 **Live Market Data** | Real-time gold, silver prices and currency exchange rates |
| 🧮 **Smart Calculators** | GST, EMI, SIP, Compound Interest, Budget Planner, Savings Goal |
| 📚 **Learning Hub** | 10+ structured financial education modules with examples |
| 📊 **Health Dashboard** | Multi-dimensional financial health scoring with charts |
| 🌐 **6 Languages** | English, Hindi, Telugu, Tamil, Kannada, Malayalam |
| 📄 **Source Citations** | Every answer backed by verified Indian financial documents |
| 🔒 **Anti-Hallucination** | Strict prompt guardrails — never fabricates financial data |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Gradio Blocks UI                   │
│  (Chat, Voice, Market, Calculators, Learning)   │
├─────────────────────────────────────────────────┤
│            Business Logic Layer                 │
│  (prompts.py, calculators.py, learning.py)      │
├─────────────────────────────────────────────────┤
│         LLM Agent Layer (LangChain)             │
│  (Google Gemini 2.5 Flash + Tool Calling)       │
├─────────────────────────────────────────────────┤
│              Tool Layer                         │
│  (tools.py, market.py, voice.py)                │
├─────────────────────────────────────────────────┤
│         Vector Database (ChromaDB)              │
│  (sentence-transformers/all-MiniLM-L6-v2)       │
├─────────────────────────────────────────────────┤
│           External APIs                         │
│  (Gemini, AssemblyAI, Murf AI, GoldAPI)         │
└─────────────────────────────────────────────────┘
```

---

## ⚡ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Gradio Blocks | Professional responsive dark UI |
| **LLM** | Google Gemini 2.5 Flash | Fast, multilingual AI inference |
| **AI Framework** | LangChain (LCEL) | Chain orchestration and tool calling |
| **Vector DB** | ChromaDB | Local vector storage for RAG |
| **Embeddings** | all-MiniLM-L6-v2 | Semantic search embeddings |
| **STT** | AssemblyAI | Speech-to-text (99 languages) |
| **TTS** | Murf AI / gTTS | Text-to-speech (Indian languages) |
| **Market Data** | GoldAPI, Frankfurter | Live prices and exchange rates |
| **Charts** | Plotly | Interactive financial visualizations |
| **Config** | python-dotenv | Secure environment management |

---

## 📁 Project Structure

```
ArthaMind-AI/
├── app.py              # Main Gradio application (UI + event handlers)
├── config.py           # Centralized configuration & environment
├── rag.py              # RAG pipeline (ChromaDB + embeddings)
├── voice.py            # Voice assistant (STT + TTS pipeline)
├── market.py           # Live market data with caching & fallback
├── tools.py            # LangChain tool definitions (9 tools)
├── prompts.py          # System prompts & anti-hallucination templates
├── calculators.py      # Pure financial calculation functions
├── learning.py         # Financial education content (10+ topics)
├── utils.py            # Logging, formatting, error handling
├── requirements.txt    # Pinned Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── LICENSE             # MIT License
├── assets/             # Static assets (images, logos)
├── data/               # Knowledge base documents
│   ├── income_tax.md           # Income tax slabs, 80C, TDS, ITR
│   ├── gst.md                  # GST rates, ITC, returns, HSN
│   ├── investments.md          # MFs, SIP, PPF, NPS, EPF, SGBs
│   └── banking_insurance_digital.md  # FD, insurance, CIBIL, UPI
└── logs/               # Application logs (auto-generated)
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ArthaMind-AI.git
cd ArthaMind-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Optional (for Voice AI)
ASSEMBLYAI_API_KEY=your_assemblyai_key
MURF_API_KEY=your_murf_key

# Optional (for Live Market Data)
GOLDAPI_KEY=your_goldapi_key
```

**Getting API Keys:**
| Service | Free Tier | Get Key |
|---------|-----------|---------|
| Google Gemini | Generous free tier | [aistudio.google.com](https://aistudio.google.com/apikey) |
| AssemblyAI | 185 hours free | [assemblyai.com](https://www.assemblyai.com/dashboard) |
| GoldAPI | Limited free calls | [goldapi.io](https://www.goldapi.io/) |
| Murf AI | $10 free credits | [murf.ai](https://murf.ai/api) |

### 5. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:7860`

---

## ☁️ Deploy to Hugging Face Spaces

### Option 1: Git Push

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces) → Select **Gradio** SDK
2. Clone and push:

```bash
git remote add hf https://huggingface.co/spaces/yourusername/ArthaMind-AI
git push hf main
```

3. Add secrets in **Settings → Secrets**:
   - `GOOGLE_API_KEY`
   - `ASSEMBLYAI_API_KEY` (optional)
   - `GOLDAPI_KEY` (optional)

### Option 2: Upload Files

Upload all project files via the Hugging Face web interface.

---

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ | Google Gemini API key |
| `ASSEMBLYAI_API_KEY` | ❌ | AssemblyAI STT key |
| `MURF_API_KEY` | ❌ | Murf AI TTS key |
| `GOLDAPI_KEY` | ❌ | GoldAPI.io key |
| `LOG_LEVEL` | ❌ | Logging level (default: INFO) |
| `GRADIO_SERVER_PORT` | ❌ | Server port (default: 7860) |
| `GRADIO_SHARE` | ❌ | Enable public sharing (default: false) |

---

## 📸 Screenshots

> *Screenshots will be added after deployment.*

| Tab | Description |
|-----|-------------|
| 💬 AI Chat | ChatGPT-like financial Q&A with source citations |
| 🎙️ Voice | Record audio → AI transcribes → responds with voice |
| 📈 Market | Live gold, silver prices and currency rates |
| 🧮 Calculators | GST, EMI, SIP, Compound Interest, Budget |
| 📚 Learning | Interactive financial education modules |
| 📊 Health | Financial health score with charts and suggestions |

---

## 🔮 Future Scope

- 📊 **Stock Market Integration** — Real-time NSE/BSE data
- 🤖 **Agentic Workflows** — Multi-step reasoning with LangGraph
- 📱 **Mobile App** — React Native companion
- 🔐 **User Auth** — Persistent profiles and history
- 📈 **Portfolio Tracker** — Track investments
- 🧠 **Fine-tuned Models** — Domain-specific Indian finance model
- 🌍 **More Languages** — Bengali, Marathi, Gujarati, Punjabi
- 📄 **Custom PDF Upload** — User-uploaded documents for RAG

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

ArthaMind AI is an **educational tool** and does NOT constitute professional financial advice. Always consult a certified financial advisor (CA, CFP) for important financial decisions. The information provided is based on publicly available Indian financial regulations and may not reflect the latest changes.

---

<div align="center">

**Built with ❤️ for the Indian financial community 🇮🇳**

*ArthaMind AI — Empowering every citizen to make smarter financial decisions with AI*

</div>
