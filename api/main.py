# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import matching, talents, missions   # ← ajoute missions

app = FastAPI(title="MindBridge AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matching.router, prefix="/api")
app.include_router(talents.router, prefix="/api")
app.include_router(missions.router, prefix="/api")   # ← ajoute ça

@app.get("/")
def root():
    return {"status": "MindBridge AI is running 🚀"}