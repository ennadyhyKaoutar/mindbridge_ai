# api/schemas.py
from pydantic import BaseModel

class MissionRequest(BaseModel):
    mission_text: str
    mission_title: str = "Mission sans titre"  # ✅ ajoute cette ligne

class TalentRequest(BaseModel):
    id: str
    cv_text: str
    name: str
    specialty: str

class CandidateResponse(BaseModel):
    rank: int
    name: str
    specialty: str
    score: float
    reason: str
    status: str

class SubtaskResponse(BaseModel):
    task: str
    profile: str
    candidates: list[CandidateResponse]

class MatchResponse(BaseModel):
    mission_title: str  # ✅ ajoute cette ligne
    subtasks: list[SubtaskResponse]