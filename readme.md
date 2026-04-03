---
title: AI Website RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
pinned: false
app_file: app.py
---

# 🤖 AI Website RAG Chatbot

An intelligent Chatbot that can scrape websites, index their content using ChromaDB, and provide context-aware answers using Google Gemini Pro.

## 🚀 Key Features
- **RAG (Retrieval-Augmented Generation)**: Uses website-specific data to answer questions accurately.
- **Web Scraper**: Extracts and cleans text from any provided URL.
- **Vector Search**: Uses `SentenceTransformers` and `ChromaDB` for high-performance retrieval.
- **Full Auth**: Secure Signup/Login system with JWT.
- **Dual Interface**: FastAPI Backend + Streamlit Frontend (starts automatically together).

## 🛠️ Project Structure (Flat)
- `app.py`: Streamlit frontend & background backend launcher.
- `main.py`: FastAPI server & route orchestration.
- `database.py`: SQLite connection & Session handling.
- `models.py`: Database tables (User, Chat, Website).
- `schemas.py`: Pydantic validation models.
- `security.py`: JWT & Password security logic.
- `scraper.py`: BeautifulSoup-based web scraper.
- `embedding_service.py`: Text-to-Vector conversion.
- `rag_service.py`: Chunking & Context-aware Answer generation.
- `vector_store.py`: Persistent ChromaDB storage.
- `llm_service.py`: General AI chat fallback.
- `auth_routes.py`, `chat_routes.py`, `website_routes.py`: API Endpoints.

## 🏃 Local Setup
1. Install dependencies: `pip install -r requirement.txt`
2. Create a `.env` file with `GEMINI_API_KEY=your_key_here`.
3. Run the app: `streamlit run app.py`

*Note: The FastAPI server will automatically start in the background when the Streamlit app is launched.*
