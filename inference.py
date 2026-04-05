from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# ROUTES (PAGES)
# =========================
from fastapi import Body
@app.post("/login")
def login(data: dict = Body(...)):
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return {"status": "success"}
    return {"status": "fail"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/dashboard.html")

# =========================
# LOGIN API (YOUR CODE ADDED HERE)
# =========================
@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return {"status": "success"}
    return {"status": "fail"}

# =========================
# RESET API (REQUIRED)
# =========================
@app.post("/reset")
def reset():
    return {"status": "ok"}
