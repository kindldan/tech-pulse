# ⚡ Tech Pulse — Real-Time IT Trends Dashboard

A real-time aggregator that parses trending repositories from **GitHub**, top stories from **Hacker News**, and best articles from **Habr**, displaying them in a single beautiful dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🐙 **GitHub Trending** — top repositories of the day with language and stars
- 🔶 **Hacker News** — top 20 stories via official Firebase API
- 💎 **Habr** — best articles from the Russian IT community
- ⚡ **Async parsing** — all sources fetched in parallel via `asyncio` + `httpx`
- 💾 **Smart caching** — 5-minute cache to avoid rate limits
- 🎨 **Modern UI** — dark theme, gradients, responsive grid layout
- 🔄 **Auto-refresh** — page updates every 5 minutes automatically
- 🔌 **REST API** — `/api/refresh` endpoint for forced data update

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| HTTP client | httpx (async) |
| Parsing | BeautifulSoup4 |
| Frontend | HTML, CSS, Jinja2 templates |
| Data sources | GitHub, Hacker News API, Habr |

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/tech-pulse.git
cd tech-pulse

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py