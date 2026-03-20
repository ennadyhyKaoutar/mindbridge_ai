# api/routes/missions.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ai.mission_decomposer import decompose_mission
from ai.matching_engine import find_best_talents

router = APIRouter()

class MissionCreateRequest(BaseModel):
    mission_title: str = "Mission sans titre"
    mission_text: str        # ✅ correspond à ce qu'envoie le frontend
    skills: List[str] = []
    deadline: str = ""

@router.post("/missions")
def create_mission(body: MissionCreateRequest):
    try:
        subtasks = decompose_mission(body.mission_text)
        results = []

        for subtask in subtasks["subtasks"]:
            profile = subtask["profile"]
            top_talents = find_best_talents(profile, top_k=5)

            results.append({
                "task": subtask["task"],
                "profile": profile,
                "candidates": [
                    {
                        "rank": i + 1,
                        "name": t["name"],
                        "specialty": t["specialty"],
                        "score": round(t["score"], 2),
                        "reason": t["reason"],
                        "status": "Available",
                    }
                    for i, t in enumerate(top_talents)
                ],
            })

        return {
            "mission_title": body.mission_title,
            "subtasks": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))