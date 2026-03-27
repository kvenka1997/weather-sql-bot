# weather-sql-bot

# 🌍 Climate & Energy SQL Agent

An AI-powered chatbot that lets you query a global climate and energy 
database using plain English — no SQL knowledge needed!

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4o--mini-purple)

## 🎯 What does it do?

You type a question in plain English like:
- *"Which country has the highest CO2 emissions?"*
- *"Show me renewable energy trends from 2020 to 2024"*
- *"Compare energy prices between USA and China"*

The AI agent automatically:
1. Understands your question
2. Writes the correct SQL query
3. Runs it on the database
4. Returns a clear human-friendly answer

## 🗄️ Dataset

- **Source:** Kaggle — Global Climate & Energy Dataset
- **Coverage:** 20 countries across 5 years (2020-2024)
- **Size:** 36,540 daily records
- **Countries:** USA, China, India, Germany, Brazil, France, 
  UK, Japan, Canada, Australia and 10 more

### Key Metrics:
| Column | Description |
|---|---|
| `avg_temperature` | Daily average temperature (°C) |
| `humidity` | Humidity percentage |
| `co2_emission` | CO2 emissions |
| `energy_consumption` | Total energy consumed |
| `renewable_share` | % of energy from renewables |
| `urban_population` | Urban population percentage |
| `industrial_activity_index` | Industrial activity score |
| `energy_price` | Energy price index |

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Streamlit** | Web interface |
| **LangChain** | AI agent framework |
| **OpenAI GPT-4o-mini** | Language model |
| **SQLite** | Database |
| **Python 3.12** | Backend |

## 🏗️ Architecture
```
User types question
        ↓
Streamlit UI captures it
        ↓
LangChain SQL Agent
        ↓
  ┌─────────────────────┐
  │ 1. List tables      │
  │ 2. Check schema     │
  │ 3. Write SQL query  │
  │ 4. Validate query   │
  │ 5. Execute query    │
  └─────────────────────┘
        ↓
Generate human answer
        ↓
Display in chat UI
```

## ✨ Features

- 💬 **Natural Language Querying** — Ask questions in plain English
- 🌍 **Country Filter** — Filter data by one or multiple countries
- 📅 **Date Range Selector** — Focus on specific time periods
- 📋 **Agent Steps Viewer** — See exactly how the agent thinks
- 🌦️ **Dynamic Weather UI** — Animated weather effects
- 🗑️ **Clear Chat** — Reset conversation anytime

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/climate-sql-agent
cd climate-sql-agent
```

**2. Create a virtual environment**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your OpenAI API key**

Create a `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

**5. Set up the database**
```bash
python3 explore_data.py
```

**6. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

## 📁 Project Structure
```
climate-sql-agent/
│
├── app.py                  # Main Streamlit application
├── explore_data.py         # Data exploration & SQLite setup
├── climate.db              # SQLite database
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API keys (not pushed to GitHub)
└── README.md               # This file
```

## ⚠️ Important

- Never push your `secrets.toml` file to GitHub
- Add `.streamlit/secrets.toml` to your `.gitignore` file

## 📝 Requirements
```
streamlit
langchain
langchain-community
langgraph
langchain-openai
pandas
```

## 🙋 Author

**Krishnan Venkatesan**  
[LinkedIn](https://linkedin.com/in/yourprofile) | 
[GitHub](https://github.com/yourusername)
```

---

**Before pushing to GitHub make sure to:**

1. Add your actual LinkedIn and GitHub links
2. Create a `.gitignore` file with this inside:
```
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc