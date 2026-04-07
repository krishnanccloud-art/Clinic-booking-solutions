from fastapi import APIRouter
from db import get_db
from models import SupportTicket
import uuid

router = APIRouter()

@router.post("/")
async def raise_ticket(ticket: SupportTicket):
    db = get_db()
    ticket_id = "TKT-" + str(uuid.uuid4())[:8].upper()
    record = {"id": ticket_id, **ticket.dict(), "status": "open"}
    db.collection("support_tickets").document(ticket_id).set(record)
    return {"message": "Ticket raised", "ticket_id": ticket_id}
