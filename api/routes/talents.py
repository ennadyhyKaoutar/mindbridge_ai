import tempfile

from fastapi import HTTPException

@router.post("/talents/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    try:
        # ✅ Utilise le dossier temp de Windows
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        cv_data = parse_cv_with_llm(tmp_path)
        os.remove(tmp_path)

        talent_id = str(uuid.uuid4())
        cv_text = f"{cv_data.get('specialty', '')} {' '.join(cv_data.get('skills', []))} {' '.join(cv_data.get('experience', []))}"

        add_talent_to_db(
            id=talent_id,
            cv_text=cv_text,
            name=cv_data.get("name", "Inconnu"),
            specialty=cv_data.get("specialty", "—"),
        )

        return {
            "success": True,
            "talent_id": talent_id,
            "parsed": cv_data,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))