"""
FastAPI server for the WellnessAgent.
Exposes a single chat endpoint that routes user messages to the agent.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from database import init_db
from agent import run_agent

app = FastAPI()

# --- Request Model ---
# Defines the shape of the incoming request body.
class ChatRequest(BaseModel):
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
    reply = run_agent(request.message)
    return {"reply": reply}