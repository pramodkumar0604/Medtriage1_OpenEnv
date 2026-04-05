from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
