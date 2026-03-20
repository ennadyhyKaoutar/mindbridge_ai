# 🧠 MindBridge AI — Intelligent Talent Matching Platform

MindBridge AI is an intelligent platform that automatically matches junior talents with business missions using semantic AI and vector search.

---

## 🚀 Features

- 🔍 **AI Mission Decomposition** — Automatically breaks down a mission into sub-tasks and required profiles using LLaMA 3.3
- 📄 **CV Parsing** — Extracts and structures data from PDF CVs using Groq
- 🎯 **Semantic Matching** — Matches talents to missions using Gemini embeddings + Pinecone vector search
- 💡 **AI Reasoning** — Generates a human-readable explanation for each match
- ⚡ **REST API** — FastAPI backend ready to connect to any frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM (decomposition, parsing, reasoning) | Groq / LLaMA 3.3 70B |
| Embeddings | Google Gemini |
| Vector Database | Pinecone |
| Backend API | FastAPI + Uvicorn |

---

## 📁 Project Structure
```
mindbridge_ai/
│
├── ai/
│   ├── embeddings.py          # Gemini embeddings + Pinecone storage
│   ├── matching_engine.py     # Talent matching logic
│   ├── mission_decomposer.py  # Mission decomposition via Groq
│   └── cv_parser.py           # CV parsing via Groq
│
├── api/
│   ├── main.py                # FastAPI app + CORS
│   ├── schemas.py             # Pydantic models
│   └── routes/
│       ├── matching.py        # POST /api/match
│       ├── missions.py        # POST /api/missions
│       └── talents.py         # POST /api/talents + upload-cv
│
├── .env.example               # Environment variables template
├── requirements.txt
└── main.py                    # Test script
```

---

## 🧪 Test Script (`main.py`)

`main.py` is a standalone test script that allows you to test the full AI pipeline without the API.

It does 3 things :

**1. Adds fictional talents to Pinecone**
```python
add_talent_to_db("1", "Finance student with experience in financial modeling...", "Ahmed", "Finance")
add_talent_to_db("4", "Marketing student specialized in market research...", "Sara", "Marketing")
# ... 13 talents across Finance, Marketing, Data, HR, Legal
```

**2. Decomposes a test mission**
```python
mission_text = """
We want to expand our business in Europe.
We need a market analysis and a financial analysis.
"""
# → [{ task: "...", profile: "Market Research Analyst" }, { task: "...", profile: "Financial Analyst" }]
```

**3. Runs matching for each profile**
```
Profile: "Market Research Analyst"
→ Top 3 matching talents from Pinecone + score + AI reason
```

**Run it with :**
```bash
python main.py
```

**Expected output :**
```
Ajout des talents dans la base...
✅ Talent Ahmed ajouté à la base.
✅ Talent Sara ajouté à la base.
...
Sous-missions extraites :
- Conduct market analysis | Profil requis: Market Research Analyst
- Perform financial analysis | Profil requis: Financial Analyst

--- Matching Talents par sous-mission ---
1. Sara (Marketing) - Score: 87.34
   Raison : Sa spécialisation en études de marché correspond directement au poste.
...
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/TON_USERNAME/mindbridge_ai.git
cd mindbridge_ai
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Fill in your API keys in `.env` :
```env
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_env
PINECONE_INDEX_NAME=mindbridge-talents
GEMINI_API_KEY=your_gemini_key
```

### 5. Run the backend
```bash
uvicorn api.main:app --reload --port 8000
```

### 6. Test the API
Open **http://localhost:8000/docs** in your browser.

---

## 🔄 How It Works
```
SME creates a mission
        ↓
AI decomposes into sub-missions + required profiles (Groq)
        ↓
For each profile → semantic search in Pinecone (top 3)
        ↓
AI generates a matching reason for each candidate (Groq)
        ↓
Results returned via API
```
```
Talent uploads CV (PDF)
        ↓
Text extraction (pypdf)
        ↓
Structured parsing (Groq) → { name, skills, experience... }
        ↓
Gemini embedding → stored in Pinecone
        ↓
Available for matching
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/missions` | Create mission + run AI matching |
| POST | `/api/match` | Direct matching from mission text |
| POST | `/api/talents` | Add talent manually |
| POST | `/api/talents/upload-cv` | Upload PDF CV → parse → store |
| GET | `/api/talents` | List all talents |

---

## 🔑 Required API Keys

| Service | Link | Free Tier |
|---|---|---|
| **Groq** | [console.groq.com](https://console.groq.com) | ✅ Free |
| **Google Gemini** | [aistudio.google.com](https://aistudio.google.com) | ✅ Free tier |
| **Pinecone** | [app.pinecone.io](https://app.pinecone.io) | ✅ Free tier |

---

