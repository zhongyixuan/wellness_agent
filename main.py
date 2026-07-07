"""
FastAPI server for the WellnessAgent.
Exposes a single chat endpoint that routes user messages to the agent.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Model ---
# Defines the shape of the incoming request body.
class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- Startup ---
# Initialize the database when the server starts.
@app.on_event("startup")
def startup():
    init_db()

# --- Endpoints ---
@app.get("/")
def root():
    return {"status": "WellnessAgent is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    reply = run_agent(request.user_id, request.message)
    return {"reply": reply}

@app.get("/weight-trend")
def weight_trend():
    from agent import get_weight_trend
    return get_weight_trend()

@app.get("/weekly-report")
def weekly_report():
    from agent import get_weekly_report
    return get_weekly_report()