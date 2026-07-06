# WellnessAgent 🌿

An AI-powered wellness assistant built with Claude and FastAPI.  
Helps users track weight, diet, and exercise through natural language conversation.

## Features

- 📊 **Weight Tracking** — Log and monitor your weight over time
- 🍱 **Food Logging** — Record meals and calorie intake
- 🏃 **Exercise Logging** — Track workouts and calories burned
- 🎯 **Goal Setting** — Set target weight and monitor progress
- 📈 **BMI Calculation** — Auto-calculated based on your height and weight
- 💡 **AI Recommendations** — Personalized advice based on your data

## Tech Stack

- **AI** — [Claude](https://anthropic.com) (claude-sonnet-4-6) via Anthropic API
- **Backend** — FastAPI + Uvicorn
- **Database** — SQLite + SQLAlchemy
- **Language** — Python 3.14

## Project Structure
wellness-agent/
├── main.py        # FastAPI server and endpoints
├── agent.py       # Claude Agent logic and tools
├── database.py    # Database models and setup
├── .env           # API keys (not committed)
└── requirements.txt

## Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd wellness-agent
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. Open Swagger UI
http://127.0.0.1:8000/docs

## Example Conversations
"我身高170公分，目標體重65公斤"
"我今天體重72公斤"
"午餐吃了雞腿便當，大概700卡"
"跑步30分鐘，消耗250卡"
"我現在距離目標還差多少？"
"給我一些減重建議"

## License

MIT