# CarePoint Clinic Booking System

A production-ready healthcare appointment booking system built with FastAPI + Firestore + GCP Cloud Run.

## Tech Stack
- **Frontend**: HTML / CSS / JS (Jinja2 templates)
- **Backend**: Python FastAPI
- **Database**: Google Firestore (Free tier)
- **Deploy 1**: GCP Cloud Run
- **Deploy 2**: AWS EC2 (Free tier)

---

## Day 1 — GCP + Firestore Setup

1. Create GCP project at https://console.cloud.google.com
2. Enable Firestore: APIs & Services → Enable "Cloud Firestore API"
3. Create Firestore database (Native mode, region: asia-south1)
4. Go to IAM → Service Accounts → Create service account
5. Grant role: "Cloud Datastore User"
6. Create JSON key → download as `serviceAccountKey.json`
7. Place `serviceAccountKey.json` in project root

Seed the doctors collection:
```bash
python seed_data/seed.py
```

---

## Day 2 — Local Backend Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

export GOOGLE_APPLICATION_CREDENTIALS="serviceAccountKey.json"
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

---

## Day 3 — Frontend

All frontend lives in `templates/index.html` + `static/`.
Open http://localhost:8000 to see the UI.

---

## Day 4 — Docker + GCP Cloud Run

```bash
# Build
docker build -t clinic-booking .
docker run -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json clinic-booking

# Push to GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/clinic-booking

# Deploy
gcloud run deploy clinic-booking \
  --image gcr.io/YOUR_PROJECT_ID/clinic-booking \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json
```

---

## Day 5 — AWS EC2 Deploy

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install Docker
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker

# Pull and run
docker pull gcr.io/YOUR_PROJECT_ID/clinic-booking
docker run -d -p 80:8080 gcr.io/YOUR_PROJECT_ID/clinic-booking
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /doctors | List all doctors |
| GET | /doctors/{id} | Get one doctor |
| POST | /appointments | Book appointment |
| GET | /appointments | All bookings (admin) |
| GET | /appointments/{phone} | Patient history |
| PUT | /appointments/{id}/cancel | Cancel |
| POST | /support | Raise ticket |
| GET | /health | Health check |

---

## Cost: $0.00
- Firestore: Free (50K reads/day)
- Cloud Run: Free (2M requests/month)
- EC2: Free Tier
- GitHub: Free
