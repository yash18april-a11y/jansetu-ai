# JanSetu AI

**B.Tech CSE major project — working development foundation (v0.1).**

A citizen-facing scheme discovery prototype with Flask APIs, MySQL models, JWT authentication, a React interface, a real TF-IDF/cosine-similarity ranking baseline, and explainable deterministic eligibility screening.

## Implemented
- Register/login with hashed passwords and JWT
- Profile editing with optional attributes
- Scheme catalog and scheme details APIs (only approved active records are exposed)
- TF-IDF ML relevance ranking and separate rule-based screening
- Saved schemes
- Responsive React dashboard
- Automated engine and API tests

## Not yet implemented
LangGraph agents, Gemini integration, RAG/FAISS, OCR, mobile app, admin workflow, scheme ingestion/version audit trail, password reset, production security hardening, deployed hosting. **No verified government schemes are preloaded.**

## Requirements
Python 3.11+, Node 20+, MySQL 8 (or Docker), Git. For production use a secure managed database, TLS, migrations, secrets management, and audited scheme content.

## Quick start (local)

1. `cd jansetu-ai`
2. `cp .env.example .env` and replace `JWT_SECRET_KEY` with a random secret (e.g. `python -c "import secrets;print(secrets.token_hex(32))"`). Set database credentials matching your MySQL instance.
3. Create a MySQL database and dedicated account, or run `docker compose up -d mysql` after defining `MYSQL_PASSWORD` and `MYSQL_ROOT_PASSWORD` in `.env`. If using Docker MySQL, set matching `DATABASE_URL` in `.env`.
4. `cd backend && python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
5. `pip install -r requirements.txt`
6. Load env vars: `set -a; source ../.env; set +a` (on Windows, set them through PowerShell or an environment loader).
7. `python init_db.py` (development only; use Alembic migrations before production)
8. `python run.py`
9. New terminal: `cd frontend && npm install && npm run dev`
10. Open `http://localhost:5173`.

### Tests
With backend dependencies installed: `cd backend && python -m pytest -q`. API tests use in-memory SQLite so MySQL is not required to run them.

### Add approved schemes
There is intentionally no public scheme creation endpoint. Insert reviewed records through an administrator-controlled database operation, recording official URL, source verification date, and supported rule fields. Never publish guessed conditions. A scheme is invisible until `active=true`.

### API routes
`GET /api/health`, `POST /api/auth/register`, `POST /api/auth/login`, `GET|PUT /api/profile`, `GET /api/schemes`, `GET /api/schemes/:id`, `POST /api/recommendations`, `POST /api/schemes/:id/eligibility`, `GET|POST /api/saved`.

### Security note
The app is an academic prototype. JWT is stored in sessionStorage (not suitable for a high-risk production threat model). Add refresh/session revocation, rate limiting, CSRF-aware cookie sessions, robust email validation, database migrations, HTTPS, audit logs, admin approval, privacy notices, and retention/deletion controls before public launch.

See `docs/PROJECT_PLAN.md` for the academic research and submission roadmap.


## Project Overview

**JanSetu AI — An Intelligent Government Scheme Recommendation and Eligibility Assistance System** is a full-stack academic project designed to help citizens discover relevant Indian government welfare schemes.

### Technology Stack

- **Frontend:** React and Vite
- **Backend:** Python, Flask and REST APIs
- **Database:** MySQL
- **Authentication:** JWT
- **Recommendation Engine:** TF-IDF and cosine similarity
- **Deployment Environment:** Docker Compose

### Key Features

1. User registration and login
2. Citizen profile management
3. Government scheme discovery and search
4. AI-assisted scheme recommendation ranking
5. Rule-based eligibility assistance
6. Save and manage schemes
7. Links to official government information portals

### How the Recommendation System Works

The recommendation engine uses TF-IDF to represent scheme descriptions and user search queries as numerical vectors. Cosine similarity ranks schemes according to textual relevance.

Eligibility assistance is evaluated separately using available rule conditions. A recommendation score does not indicate an applicant's probability of approval.

### Scheme Dataset

The project database contains 25 scheme records:

- 5 published scheme entries
- 20 unpublished draft entries awaiting review

Only published schemes are displayed to citizens. Scheme eligibility conditions, official URLs and government policies must be verified before additional entries are published.

### Running the Application

1. Install Docker Desktop and Node.js.
2. Create a `.env` file using `.env.example` as a guide and configure strong secrets.
3. Start the backend and database:

   `docker compose up -d --build`

4. Open a terminal in the `frontend` directory.
5. Install dependencies:

   `npm install`

6. Start the frontend:

   `npm run dev`

7. Open `http://localhost:5173`.

### Testing

Backend tests:

`docker compose exec api python -m pytest -q`

Frontend production build:

`npm run build`

The project has passed seven backend automated tests and seven manual core-feature checks during local development.

### Limitations

JanSetu AI is an academic prototype, not an official government service. Recommendations are informational, and eligibility results are preliminary. Users must confirm current requirements and decisions with the relevant official government authority.

### Future Scope

- Multilingual support
- Expanded verified scheme database
- More comprehensive eligibility rules
- Mobile application
- Secure production deployment