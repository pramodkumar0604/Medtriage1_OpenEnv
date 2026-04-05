from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI(title="MedTriage Advanced")

app.mount("/static", StaticFiles(directory="static"), name="static")

DATA_FILE = "data.json"

# Load history
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save history
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.get("/")
def home():
    return FileResponse("templates/index.html")

@app.get("/history")
def history():
    return load_data()

# ✅ RESET endpoint (must be OUTSIDE predict)
@app.post("/reset")
def reset():
    return {"status": "ok"}

# ✅ FIXED predict function
@app.post("/predict")
def predict(data: dict):
    symptoms = data.get("symptoms", "").lower()
    age = int(data.get("age", 0))

    # ML-like scoring
    score = 0

    if "fever" in symptoms:
        score += 2
    if "cough" in symptoms:
        score += 2
    if "chest pain" in symptoms:
        score += 3
    if "fatigue" in symptoms:
        score += 1
    if age > 60:
        score += 2

    if score >= 5:
        risk = "HIGH"
        advice = "Consult doctor immediately"
    elif score >= 3:
        risk = "MEDIUM"
        advice = "Monitor symptoms"
    else:
        risk = "LOW"
        advice = "No major issue"

    record = {
        "age": age,
        "symptoms": symptoms,
        "risk": risk
    }

    history = load_data()
    history.append(record)
    save_data(history)

    return {
        "risk_level": risk,
        "advice": advice
    }
