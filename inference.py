from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json, os

app = FastAPI()

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

DATA_FILE = "data.json"

# ---------- HELPERS ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------- ROUTES ----------

# Login page
@app.get("/")
def login_page():
    return FileResponse("templates/login.html")

# Login action → redirect to dashboard
@app.post("/login")
def login():
    return FileResponse("templates/dashboard.html")

# Dashboard page
@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/dashboard.html")

# Get patient history
@app.get("/history")
def history():
    return load_data()

# Predict risk
@app.post("/predict")
def predict(data: dict):
    symptoms = data.get("symptoms", "").lower()
    age = int(data.get("age", 0))

    score = 0

    if "fever" in symptoms:
        score += 2
    if "cough" in symptoms:
        score += 2
    if "fatigue" in symptoms:
        score += 1
    if age > 60:
        score += 2

    if score >= 5:
        risk = "HIGH"
    elif score >= 3:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    record = {
        "age": age,
        "symptoms": symptoms,
        "risk": risk
    }

    history_data = load_data()
    history_data.append(record)
    save_data(history_data)

    return {
        "risk_level": risk,
        "advice": "Consult doctor if needed"
    }

# REQUIRED for OpenEnv
@app.post("/reset")
def reset():
    return {"status": "ok"}
