# 🧠 Web Summarizer using LLMs

This is a full-stack AI-powered web summarization application.  
It extracts main content from any webpage and summarizes it using OpenAI's GPT models.

Built with:
- ⚛️ React (Frontend)
- 🎨 Tailwind CSS (Styling)
- 🧠 Python Flask (Backend)
- 🤖 OpenAI GPT API
- 🔍 BeautifulSoup (HTML parsing)

---

## 🌐 Live Flow

1. User enters a URL into the frontend
2. React sends the URL to the Flask backend via POST `/summarize`
3. Flask:
   - Scrapes and cleans the webpage using BeautifulSoup
   - Truncates long text to fit model token limits
   - Sends cleaned content to OpenAI (gpt-3.5-turbo or gpt-4o)
4. Receives and returns summary to the frontend
5. User sees the summary in real-time

---

## 📁 Project Structure

```
web-summarizer/
├── backend/
│   ├── backend.py              # Flask backend code
│   ├── .env                    # OpenAI API key
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main frontend logic
│   │   ├── index.css           # Tailwind styles
│   │   └── index.js            # React root
│   ├── public/
│   │   └── index.html
│   ├── package.json            # React app config
│   ├── tailwind.config.js
│   └── postcss.config.js
```

---

## 🚀 Quick Start

### 🧪 Backend (Flask + OpenAI)

#### 1. Setup

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Create `.env` file

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. Run the backend

```bash
python backend.py
```

It runs at: `http://localhost:5000`

---

### 🌐 Frontend (React + Tailwind CSS)

#### 1. Setup

```bash
cd frontend
npm install
```

#### 2. Start React server

```bash
npm start
```

Runs at: `http://localhost:3000`

---

## 🧠 API Reference

### `POST /summarize`

**Request:**

```json
{
  "url": "https://en.wikipedia.org/wiki/OpenAI"
}
```

**Response:**

```json
{
  "summary": "OpenAI is a leading research lab focused on developing AI responsibly..."
}
```

---

## 🔥 Features

- ✂️ Automatically removes navbars, footers, ads from scraped pages
- 📄 Supports large inputs (with token-limited truncation)
- 💬 Uses OpenAI’s GPT for accurate, clean summaries
- 💻 Fully styled frontend with TailwindCSS
- 🧠 Easily extendable for PDF, text input, or local LLMs

---

## 📌 Future Ideas

- 🔁 Add support for bullet-point vs paragraph summaries
- 📄 Export summaries to PDF or Markdown
- 🧠 Add local model support with Ollama or Llama.cpp
- 🌍 Deploy backend (Render, Railway) and frontend (Vercel, Netlify)

---

## 📄 License

MIT License  
Built with 💙 by [Your Name](https://github.com/yourusername)
