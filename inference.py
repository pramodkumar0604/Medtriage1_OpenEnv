from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="MedTriage API")

# UI setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
def predict(data: dict):
    symptoms = data.get("symptoms", "").lower()

    # Simple MedTriage logic
    if "fever" in symptoms and "cough" in symptoms:
        result = "⚠️ Possible infection (Consult doctor)"
    elif "headache" in symptoms:
        result = "🟡 Mild condition (Rest recommended)"
    else:
        result = "🟢 Low risk"

    return {
        "triage_result": result,
        "input": symptoms
    }