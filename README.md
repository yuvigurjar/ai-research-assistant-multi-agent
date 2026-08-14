# 🧠 AI Research Assistant - Multi-Agent

A multi-agent AI research assistant built with LangChain, Mistral AI, Tavily, BeautifulSoup, and Streamlit.

The application automatically researches a given topic through a four-step pipeline:

**Search → Read → Write → Critique**

---

## 🚀 Features

- 🔎 Web search using Tavily
- 📖 Web page scraping using BeautifulSoup
- 🤖 Multi-agent architecture using LangChain
- 🧠 Mistral AI-powered agents
- ✍️ Automated research report generation
- 🧐 AI-powered report criticism and scoring
- 📊 Streamlit web interface
- ⬇️ Download generated reports as Markdown
- 🔐 Environment variable based API key management

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              Streamlit App
                  app.py
                     │
                     ▼
             Research Pipeline
                pipeline.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Search Agent           Reader Agent
      Tavily               Web Scraping
          │                     │
          └──────────┬──────────┘
                     ▼
                Writer Chain
                     │
                     ▼
                Research Report
                     │
                     ▼
                Critic Chain
                     │
                     ▼
              Final Evaluation
