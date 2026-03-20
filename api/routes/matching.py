# api/routes/matching.py
from fastapi import APIRouter, HTTPException
from api.schemas import MissionRequest, MatchResponse
from ai.mission_decomposer import decompose_mission
from ai.matching_engine import find_best_talents

router = APIRouter()

@router.post("/match", response_model=MatchResponse)
def match_mission(body: MissionRequest):
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
    "mission_title": body.mission_title,  # ✅ ajoute cette ligne
    "subtasks": results
}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))