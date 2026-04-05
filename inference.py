from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
import pickle

app = FastAPI(title="MedTriage Pro")

# =========================
# STATIC FILES
# =========================
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# LOAD ML MODEL
# =========================
model = pickle.load(open("model.pkl", "rb"))

# =========================
# DATA STORAGE
# =========================
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# =========================
# ROUTES (PAGES)
# =========================
@app.get("/")
def login_page():
    return FileResponse("templates/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/dashboard.html")

# =========================
# LOGIN SYSTEM
# =========================
@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return {"status": "success"}
    return {"status": "fail"}

# =========================
# ENCODE FEATURES
# =========================
def encode(symptoms, age):
    return [[
        int("fever" in symptoms),
        int("cough" in symptoms),
        int("chest pain" in symptoms),
        int("fatigue" in symptoms),
        int(age > 60)
    ]]

# =========================
# PREDICT (ML)
# =========================
@app.post("/predict")
def predict(data: dict):
    symptoms = data.get("symptoms", "").lower()
    age = int(data.get("age", 0))

    features = encode(symptoms, age)
    risk = model.predict(features)[0]

    advice = {
        "HIGH": "Consult doctor immediately",
        "MEDIUM": "Monitor symptoms",
        "LOW": "No major issue"
    }[risk]

    # Save history
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

# =========================
# HISTORY API
# =========================
@app.get("/history")
def history():
    return load_data()

# =========================
# RESET API (IMPORTANT FOR OPENENV)
# =========================
@app.post("/reset")
def reset():
    return {"status": "ok"}

# =========================
# MAIN ENTRY (IMPORTANT 🚨)
# =========================
def main():
    import uvicorn
    uvicorn.run("inference:app", host="0.0.0.0", port=7860)

# Required for OpenEnv
if __name__ == "__main__":
    main()
