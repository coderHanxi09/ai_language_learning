# AI Reading Workspace — Backend (Minimal MVP)

This is a minimal FastAPI scaffold implementing parts of the System Architecture and PRD.

Quickstart

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints

- `GET /` — health
- `GET /dictionary/{word}` — dictionary lookup (mock)
- `POST /ai/readings` — generate a reading with Gemini (background task)

This scaffold supports connecting to a real Postgres database (such as Supabase) via the `DATABASE_URL` environment variable. If `DATABASE_URL` is not set or points to SQLite, the app will use a local SQLite file (`./dev.db`).

To use Supabase/Postgres, set `DATABASE_URL` in your `.env` to the Supabase Postgres connection string (keep credentials secret). Example:

```env
DATABASE_URL=postgresql://<user>:<password>@db.<project>.supabase.co:5432/postgres
```

At startup the app will create tables (if not present) and seed minimal dictionary entries. Replace or extend the seeding process and add migrations for production use.

Gemini integration is implemented in [app/services/ai_service.py](/Users/Hannah/Documents/THA/ai%20language%20learning%20project/backend/app/services/ai_service.py) using the official `google-generativeai` SDK.

Set these optional variables as needed:

```env
GEMINI_API_KEY=<your key>
GEMINI_MODEL=models/gemini-2.5-pro
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=800
```

Database migrations
-------------------
This project includes Alembic scaffolding. To create migrations:

```bash
pip install -r requirements.txt
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

Note: Alembic reads `DATABASE_URL` from `app.db.DATABASE_URL` at runtime via the `alembic/env.py` configuration.

Production deployment notes
--------------------------
- Do NOT use SQLite in production. Use Supabase/Postgres and secure the connection string.
- Use environment variables for secrets; do not commit `.env` with real keys.
- Run Alembic migrations during deployment to update schema.
- Put the FastAPI app behind a process manager (Gunicorn/UVicorn workers) and a reverse proxy or load balancer.
- Use background workers for AI calls and analytics processing.
