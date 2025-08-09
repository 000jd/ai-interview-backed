## AI Interview Platform Backend

Production-ready FastAPI backend for AI-powered technical and behavioral interviews, with LiveKit for real-time voice/video and an agent service that conducts interviews, asks questions, and scores responses.

### Features
- **Auth (JWT) with blocklist:** Login/logout with token revocation and `exp` handling
- **API Keys:** Create/manage keys for integrations
- **Interviews:** Create/list/update interviews; server-generated LiveKit room names
- **LiveKit integration:** Room creation and participant tokens
- **AI Agent service:** LiveKit Agents runner; welcome message and function tools
- **Config & DX:** `.env.example`, SQLite defaults, env-driven CORS, Scalar docs

### Architecture
- **FastAPI API** (`app/main.py`): REST API, auth, CRUD
- **LiveKit Manager** (`app/core/livekit_manager.py`): creates rooms, builds tokens
- **Agents Service** (`app/agents/run.py`): LiveKit Agents worker running the interview agent
- **Database** (`app/db/database.py`, `app/db/models.py`): SQLAlchemy ORM

---

## Getting Started

### Prerequisites
- Python 3.11+
- `uv` package manager (`pip install uv` or see uv docs)
- A LiveKit project (Cloud or self-hosted) with `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Optional AI providers: Google Gemini, Deepgram, ElevenLabs

### Install
```bash
git clone <repository-url>
cd ai-interview-backed
uv venv
uv sync
```

### Configure env
Copy and edit your environment:
```bash
cp .env.example .env
```
Key settings:
- `DATABASE_URL`: default SQLite is fine for local; use Postgres in prod
- `SECRET_KEY`: change in production
- `ALLOWED_ORIGINS`: set your frontend origin(s) for CORS (comma-separated)
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`: required for rooms/tokens
- Optional AI keys: `GOOGLE_API_KEY`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`

Tables are auto-created at startup; no migrations are required for local dev.

---

## Run the API
Dev server with auto-reload:
```bash
uv run uvicorn app.main:app --reload
```

Health and docs:
- Root: `http://127.0.0.1:8000/`
- Scalar: `http://127.0.0.1:8000/scalar`
- Swagger UI: `http://127.0.0.1:8000/docs`

All API endpoints are under `/api/v1`.

---

## Run the Agent Service
The agent runs as a LiveKit Agents worker. It uses env `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`.

```bash
uv run python -m app.agents.run
```

What it does:
- Prewarms models (VAD)
- Starts an `AgentSession` for the room provided by LiveKit
- Sends a welcome message and drives the interview using tools

Tip: ensure a room exists (created by the backend on interview creation) and your client joins the room using a token from the backend. The agent will join the same room and interact.

---

## Typical Flow
1) Register and login to get a JWT
2) Create an interview (`POST /api/v1/interviews/`)
   - The backend generates a unique `room_name` and creates a LiveKit room
3) Generate a participant token (`POST /api/v1/interviews/{interview_id}/token`)
4) Client joins the room with LiveKit SDK using the token
5) Agent worker connects to the room and runs the interview

For integrations, use API keys:
- Create a key (`POST /api/v1/api-keys/`)
- Create an interview via key (`POST /api/v1/interviews/api/create`)
- Generate a token via key (`POST /api/v1/interviews/api/{interview_id}/token`)

---

## Configuration Notes
- **CORS**: controlled by `ALLOWED_ORIGINS` (comma-separated). Use `*` only in dev
- **JWT**: `exp` is an integer timestamp; tokens support blocklisting on logout
- **Cleanup**: expired blocklisted tokens can be purged via `crud.cleanup_expired_blocklisted_tokens(db)` in a scheduled job

---

## Testing
```bash
uv run pytest -q
```

---

## Production
- Use Postgres for `DATABASE_URL`
- Set strong `SECRET_KEY`
- Set `ALLOWED_ORIGINS` to your exact frontend origins
- Run the API behind a reverse proxy (e.g., nginx) and a process manager (e.g., systemd, supervisord)
- Run the Agent service separately with the same env (scale workers as needed)

---

## Troubleshooting
- LiveKit errors: verify `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` and that the room exists
- Token issues: ensure client sends `Authorization: Bearer <jwt>` and that the token is not blocklisted/expired
- CORS blocked: set correct `ALLOWED_ORIGINS`