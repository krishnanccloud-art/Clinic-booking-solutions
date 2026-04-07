from fastapi import APIRouter, HTTPException
from db import get_db
from models import AppointmentCreate
import uuid

router = APIRouter()

@router.post("/")
async def book_appointment(appt: AppointmentCreate):
    db = get_db()
    doctor = db.collection("doctors").document(appt.doctor_id).get()
    if not doctor.exists:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc_data = doctor.to_dict()
    appt_id = "APT-" + str(uuid.uuid4())[:8].upper()

    record = {
        "id": appt_id,
        "doctor_id": appt.doctor_id,
        "doctor_name": doc_data["name"],
        "specialty": doc_data["specialty"],
        "patient_name": appt.patient_name,
        "phone": appt.phone,
        "age": appt.age,
        "gender": appt.gender,
        "slot_time": appt.slot_time,
        "symptoms": appt.symptoms,
        "status": "confirmed",
    }

    db.collection("appointments").document(appt_id).set(record)
    return {"message": "Appointment booked", "appointment_id": appt_id, **record}

@router.get("/")
async def all_appointments():
    db = get_db()
    docs = db.collection("appointments").stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

@router.get("/{phone}")
async def patient_appointments(phone: str):
    db = get_db()
    docs = db.collection("appointments").where("phone", "==", phone).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

@router.put("/{appt_id}/cancel")
async def cancel_appointment(appt_id: str):
    db = get_db()
    ref = db.collection("appointments").document(appt_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Appointment not found")
    ref.update({"status": "cancelled"})
    return {"message": "Appointment cancelled", "id": appt_id}
