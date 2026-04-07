from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import doctors, appointments, support

app = FastAPI(title="CarePoint Clinic Booking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(support.router, prefix="/support", tags=["Support"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "CarePoint Clinic API"}

@app.get("/")
async def root(request):
    from fastapi.requests import Request
    return templates.TemplateResponse("index.html", {"request": request})
