# WellnessAgent 🌿

An AI-powered wellness assistant built with Claude and FastAPI.  
Helps users track weight, diet, and exercise through natural language conversation.

## Features

- 💬 **Conversational Interface** — Chat naturally in Chinese with the AI agent
- 🧠 **Conversation Memory** — Agent remembers context per user
- 📊 **Weight Tracking** — Log and monitor your weight over time
- 🍱 **Food Logging** — Record meals and calorie intake
- 🏃 **Exercise Logging** — Track workouts and calories burned
- 🎯 **Goal Setting** — Set target weight and monitor progress
- 📈 **BMI Calculation** — Auto-calculated based on your height and weight
- 📉 **Weight Trend Chart** — Visualize your weight changes over time
- 📅 **Weekly Report** — Summary of weight change, calorie intake, and exercise
- 💡 **AI Recommendations** — Personalized advice based on your data

## Tech Stack

- **AI** — Claude (claude-sonnet-4-6) via Anthropic API
- **Backend** — FastAPI + Uvicorn
- **Database** — SQLite + SQLAlchemy
- **Frontend** — HTML + Tailwind CSS + Chart.js
- **Language** — Python 3.14

## Project Structure

```
wellness-agent/
├── main.py          # FastAPI server and endpoints
├── agent.py         # Claude Agent logic and tools
├── database.py      # Database models and setup
├── index.html       # Web UI (chat + charts + reports)
├── .env             # API keys (not committed)
├── .env.example     # Template for environment variables
├── requirements.txt # Python dependencies
└── README.md
```

## Getting Started

### 1. Clone the repo

```bash
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

### 6. Open the web UI

Open `index.html` in your browser, or visit Swagger UI for API testing:
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Send a message to the agent |
| GET | `/weight-trend` | Get weight records for chart |
| GET | `/weekly-report` | Get weekly summary data |

## Available Agent Tools

The agent can autonomously call these tools based on user requests:

| Tool | Purpose |
|------|---------|
| `set_user_goal` | Set height and target weight |
| `log_weight` | Record daily weight |
| `log_food` | Log meals with calories |
| `log_exercise` | Track workouts |
| `get_daily_summary` | Today's calorie summary |
| `check_progress` | Distance to target + BMI |
| `get_weight_trend` | Weight history for visualization |
| `get_weekly_report` | Weekly statistics |
| `get_recommendation` | AI-generated advice |

## Example Conversations
"我身高170公分，目標體重65公斤"
"我今天體重72公斤"
"午餐吃了雞腿便當，大概700卡"
"跑步30分鐘，消耗250卡"
"我現在距離目標還差多少？"
"給我一些減重建議"

## License

MIT