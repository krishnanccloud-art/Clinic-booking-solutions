from fastapi import APIRouter, HTTPException
from db import get_db

router = APIRouter()

@router.get("/")
async def list_doctors():
    db = get_db()
    docs = db.collection("doctors").stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str):
    db = get_db()
    doc = db.collection("doctors").document(doctor_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"id": doc.id, **doc.to_dict()}
