"""
Core logic for the WellnessAgent.
Defines tools, implements tool functions, and runs the agent loop.
"""

import os
import json
from anthropic import Anthropic
from database import SessionLocal, UserGoal, WeightLog, FoodLog, ExerciseLog
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

# --- Tool Definitions ---
# The "menu" that tells Claude what tools are available and what parameters they need.

tools = [
    {
        "name": "set_user_goal",
        "description": "設定使用者的身高和目標體重",
        "input_schema": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "number",
                    "description": "身高，單位 cm"
                },
                "target_weight": {
                    "type": "number",
                    "description": "目標體重，單位 kg"
                }
            },
            "required": ["height", "target_weight"]
        }
    },
    {
        "name": "log_weight",
        "description": "記錄今日體重",
        "input_schema": {
            "type": "object",
            "properties": {
                "weight": {
                    "type": "number",
                    "description": "體重，單位 kg"
                }
            },
            "required": ["weight"]
        }
    },
    {
        "name": "log_food",
        "description": "記錄飲食，包含食物名稱、熱量和餐別",
        "input_schema": {
            "type": "object",
            "properties": {
                "food_name": {
                    "type": "string",
                    "description": "食物名稱，例如：雞腿便當、拿鐵"
                },
                "calories": {
                    "type": "number",
                    "description": "熱量，單位 kcal"
                },
                "meal_type": {
                    "type": "string",
                    "enum": ["breakfast", "lunch", "dinner", "snack"],
                    "description": "餐別"
                }
            },
            "required": ["food_name", "calories", "meal_type"]
        }
    },
    {
        "name": "log_exercise",
        "description": "記錄運動，包含運動名稱、時間和消耗熱量",
        "input_schema": {
            "type": "object",
            "properties": {
                "exercise_name": {
                    "type": "string",
                    "description": "運動名稱，例如：跑步、重訓、游泳"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "運動時間，單位分鐘"
                },
                "calories_burned": {
                    "type": "number",
                    "description": "消耗熱量，單位 kcal"
                }
            },
            "required": ["exercise_name", "duration_minutes", "calories_burned"]
        }
    },
    {
        "name": "get_daily_summary",
        "description": "取得今日飲食和運動的熱量總結",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "check_progress",
        "description": "檢查目前體重距離目標還差多少，以及目前的BMI",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_recommendation",
        "description": "根據使用者目前的體重、BMI、飲食和運動記錄，給出減重建議",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

# --- Tool Implementation ---
# Each function corresponds to a tool definition above.

def set_user_goal(height: float, target_weight: float):
    db = SessionLocal()
    goal = UserGoal(height=height, target_weight=target_weight)
    db.add(goal)
    db.commit()
    db.close()
    return {"status": "success", "message": f"已設定身高 {height}cm, 目標體重 {target_weight}kg"}

def log_weight(weight: float):
    db = SessionLocal()
    log = WeightLog(weight=weight)
    db.add(log)
    db.commit()
    db.close()
    return {"status": "success", "message": f"已紀錄體重 {weight}kg"}

def log_food(food_name: str, calories: float, meal_type: str):
    db = SessionLocal()
    log = FoodLog(food_name=food_name, calories=calories, meal_type=meal_type)
    db.add(log)
    db.commit()
    db.close()
    return {"status": "success", "message": f"已記錄 {meal_type}：{food_name}，{calories} kcal"}

def log_exercise(exercise_name: str, duration_minutes: int, calories_burned: float):
    db = SessionLocal()
    log = ExerciseLog(exercise_name=exercise_name, duration_minutes=duration_minutes, calories_burned=calories_burned)
    db.add(log)
    db.commit()
    db.close()
    return {"status": "success", "message": f"已記錄 {exercise_name} {duration_minutes} mins，消耗 {calories_burned} kcal"}

def get_daily_summary():
    db = SessionLocal()
    today = datetime.now().date()

    # Filter today's food and exercise logs
    foods = db.query(FoodLog).filter(FoodLog.date >= today).all()
    exercises = db.query(ExerciseLog).filter(ExerciseLog.date >= today).all()
    db.close()

    total_intake = sum(f.calories for f in foods)
    total_burned = sum(e.calories_burned for e in exercises)

    return {
        "total_intake_kcal": total_intake,
        "total_burned_kcal": total_burned,
        "net_calories": total_intake - total_burned,
        "foods": [{"name": f.food_name, "calories": f.calories, "meal": f.meal_type} for f in foods],
        "exercises": [{"name": e.exercise_name, "duration": e.duration_minutes, "burned": e.calories_burned} for e in exercises]
    }

def check_progress():
    db = SessionLocal()

    # Get latest weight and goal
    latest_weight = db.query(WeightLog).order_by(WeightLog.date.desc()).first()
    goal = db.query(UserGoal).order_by(UserGoal.created_at.desc()).first()
    db.close()

    if not latest_weight or not goal:
        return {"status": "error", "message": "請先設定目標體重和身高，並記錄至少一次體重"}

    weight = latest_weight.weight
    height_m = goal.height / 100
    bmi = round(weight / (height_m ** 2), 1)
    diff = round(weight - goal.target_weight, 1)

    return {
        "current_weight": weight,
        "target_weight": goal.target_weight,
        "difference": diff,        # 正數代表還需減重，負數代表已達標
        "bmi": bmi,
        "bmi_status": "過重" if bmi >= 25 else "正常" if bmi >= 18.5 else "過輕"
    }

def get_recommendation():
    # Gather all data and let Claude generate recommendations
    summary = get_daily_summary()
    progress = check_progress()

    return {
        "daily_summary": summary,
        "progress": progress
    }

# --- Tool Execution ---
# Translates Claude's tool call decisions into actual function calls.

def run_tool(name: str, inputs: dict):
    if name == "set_user_goal":
        return set_user_goal(**inputs)
    elif name == "log_weight":
        return log_weight(**inputs)
    elif name == "log_food":
        return log_food(**inputs)
    elif name == "log_exercise":
        return log_exercise(**inputs)
    elif name == "get_daily_summary":
        return get_daily_summary()
    elif name == "check_progress":
        return check_progress()
    elif name == "get_recommendation":
        return get_recommendation()

# --- Agent Main Loop ---
# Sends user message to Claude, executes tools when needed,
# and loops until Claude returns a final response.

def run_agent(user_message: str) -> str:
    # Create conversation history
    messages = [{"role": "user", "content": user_message}]

    # This system prompt tells Claude its role and behavior guidelines. It's included with every API call.
    system = """你是一個專業的健康管理助理 WellnessAgent。
    幫助使用者記錄和追蹤體重、飲食和運動。
    用繁體中文回覆，語氣親切但專業。
    提供建議時請根據實際數據，不要給過於激進的減重建議。
    體重單位是公斤，熱量單位是大卡。"""

    while True:
        response=client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages
        )

        # Claude is done, return the final response
        if response.stop_reason == "end_turn":
            return response.content[0].text
        
        # Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Append Claude's response to conversation
            messages.append({"role": "assistant", "content": response.content})

            # Execute all requested tools and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # Send tool results back to Claude
            messages.append({"role": "user", "content": tool_results})