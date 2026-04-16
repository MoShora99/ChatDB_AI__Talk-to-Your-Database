# ChatDB AI --- Talk to Your Database

ChatDB AI is a conversational interface that lets you interact with your
PostgreSQL database using **plain natural language**. No SQL, no
complexity --- just ask, and the AI handles the rest.\
Built using **FastAPI, PostgreSQL, pgvector, HTML/CSS/JS, and GiminAI
LLM**.
## 🤝 Project Preview

-⚠️ The project is currently running locally and not deployed yet.
Below are screenshots showing how the application works.
![Project Preview](images/1.PNG)

## 🚀 Features

-   Natural language chat interface\
-   Automatic SQL generation using GiminAI\
-   Clean and fast FastAPI backend\
-   Simple and modern frontend (HTML/CSS/JS)\
-   pgvector-powered semantic search\
-   Safe query execution with validation\
-   Supports query, insert, update, delete\
-   Modular and easy to extend

## 🧠 How It Works

You type a message like:\
- "Show me all users created this week."\
- "Add a new order for user 12 with amount 150."\
- "Update product 5 price to 120."\
- "Create a table for activity logs."

The system sends your text to the LLM → generates SQL → validates it →
executes on PostgreSQL → returns results in chat.

## 🏗️ Tech Stack

  Part            Technology
  --------------- -----------------------
  Backend         FastAPI
  Database        PostgreSQL
  Vector Search   pgvector
  LLM             GiminAI
  Frontend        HTML, CSS, JavaScript
  API             REST

## 📁 Project Structure

    project/
     ├── backend/
     │   ├── main.py
     │   ├── db.py
     │   ├── llm/
     │   └── utils/
     ├── frontend/
     │   ├── index.html
     │   ├── style.css
     │   └── app.js
     ├── embeddings/
     ├── requirements.txt
     └── README.md

## ⚙️ Installation & Setup

### 1. Clone the repository

    git clone https://github.com/yourusername/chatdb-ai.git
    cd chatdb-ai

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Enable pgvector extension in PostgreSQL

    CREATE EXTENSION IF NOT EXISTS vector;

### 4. Configure environment variables

Create a `.env` file or export them:

    GIMINAI_API_KEY=your_api_key
    DATABASE_URL=postgresql://user:password@localhost/yourdb

### 5. Run the backend

    uvicorn backend.main:app --reload

### 6. Launch the frontend

Open:

    frontend/index.html

## 💬 Example Prompts

-   "List all products sorted by price."\
-   "Show all orders for user 10."\
-   "Delete user 22."\
-   "Insert a new customer named John Doe with email test@test.com."

## 🔮 Roadmap

-   Authentication system\
-   Dashboard for analytics\
-   Multi-database support\
-   Realtime logs and monitoring

## 🤝 Contributing

Contributions, feature requests, and pull requests are always welcome.

## 📄 License

MIT License
