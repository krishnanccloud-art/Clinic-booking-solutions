from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    pending = "pending"

class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    available: bool = True
    slots: list[str] = []

class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_name: str
    phone: str
    age: int
    gender: str
    slot_time: str
    symptoms: Optional[str] = ""

class Appointment(AppointmentCreate):
    id: str
    status: AppointmentStatus = AppointmentStatus.confirmed
    doctor_name: str
    specialty: str

class SupportTicket(BaseModel):
    name: str
    phone: str
    category: str
    description: str
