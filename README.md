# AI Interview Platform Backend

This is the backend for the AI Interview Platform, a powerful, enterprise-grade application designed to streamline the technical and behavioral interview process using AI.

## Features

- **User Authentication:** Secure user registration and login using JWT.
- **API Key Management:** Generate and manage API keys for external integrations.
- **Interview Management:** Create, manage, and retrieve interview sessions.
- **LiveKit Integration:** Real-time video and audio capabilities for conducting live interviews.
- **AI-Powered Interviews:** An AI agent to conduct interviews, ask questions, and score responses.
- **Dynamic Prompts:** A flexible prompt management system to tailor interviews for different job positions.
- **API Documentation:** Interactive API documentation powered by Scalar.

## Technology Stack

- **Backend:** Python with FastAPI
- **Database:** PostgreSQL (with SQLAlchemy for ORM)
- **Real-time Communication:** LiveKit
- **Authentication:** JWT (python-jose) and bcrypt (passlib)
- **AI Services:**
  - **STT:** Deepgram
  - **LLM:** Google Gemini
  - **TTS:** ElevenLabs
- **Package Manager:** uv

## Getting Started

### Prerequisites

- Python 3.11+
- `uv` package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-interview-backed
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv
   uv sync
   ```

3. **Set up your environment variables:**

   Create a `.env` file by copying the `.env.example` file:
   ```bash
   cp .env.example .env
   ```

   Then, fill in the required values in the `.env` file, such as your database URL and API keys for LiveKit and the various AI services.

### Running the Application

To run the application in development mode with auto-reload, use the following command:

```bash
uv run uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- **Scalar:** [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

All API endpoints are versioned and available under the `/api/v1` prefix.