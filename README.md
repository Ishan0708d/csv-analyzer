# CSV Analyzer

A full-stack CSV analysis application with:
- **Django REST Framework backend**
- **React web frontend**
- **PyQt5 desktop frontend**

The app allows users to authenticate, upload CSV files containing equipment data, and receive summarized insights and visualizations.  
Both frontends consume the same backend API.

---

## Project Structure

csv-analyzer/
├── backend/ # Django + DRF backend
├── frontend_r/ # React web frontend
├── frontend_p/ # PyQt5 desktop frontend
├── .gitignore
└── README.md

## Prerequisites

Make sure you have the following installed:

- Python **3.10+**
- pip
- Node.js **18+**
- npm
- Git

---

## Backend Setup (Django + DRF)

1. Navigate to backend
2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pandas

4. Run migrations
python manage.py migrate

5. Create superuser (optional)
python manage.py createsuperuser

6. Start backend server
python manage.py runserver

Backend will run at:
http://127.0.0.1:8000/

API Endpoints:
POST /api/token/ → Login (JWT)
POST /api/token/refresh/ → Refresh token
POST /api/register/ → Register user
POST /api/upload/ → Upload CSV (authenticated)
GET /api/health/ → Health check



React Frontend Setup (Web)
1. Navigate to React frontend
cd frontend_r

2. Install dependencies
npm install

3. Start development server
npm start

React app will run at:
http://localhost:3000/

PyQt5 Frontend Setup (Desktop)
1. Navigate to PyQt frontend
cd frontend_p

2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install requests PyQt5 matplotlib

4. Run the desktop app
python app.py

CSV Format Requirements
The uploaded CSV should contain at least the following columns:
Equipment Name
Type
Flowrate
Pressure
Temperature


Features
JWT authentication (shared across frontends)
CSV upload & analysis
Summary statistics
Equipment type distribution charts
Upload history (last 5 datasets)
Clickable dataset history (React + PyQt)
Token persistence & logout cleanup


Notes
SQLite is used for local development.
No secrets or tokens are committed to the repository.
Backend must be running before using either frontend.


Future Improvements
Deployment (Vercel + cloud backend)
Per-user persistent upload history
Dataset comparison
Export reports
Dark mode

License
This project is for educational and internal use.
