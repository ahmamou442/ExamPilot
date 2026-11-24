# ✦ ExamPilot

**Understand · Test · Improve**

ExamPilot is an AI-powered learning workspace that helps students understand their courses, identify knowledge gaps, learn difficult concepts, and evaluate their progress.

## Features

- **Course Upload:** Upload one or multiple text-based PDF files.
- **Course Analysis:** Extract course content and generate a structured knowledge map.
- **Knowledge Diagnosis:** Evaluate what the student understands and identify areas that need improvement.
- **Personalized Teaching:** Teach concepts through the Motivate → Establish → Connect → Verify methodology.
- **Exam Generation:** Generate course-based practice examinations.
- **Automatic Grading:** Evaluate submitted answers and provide results.
- **Study Recommendations:** Help students prioritize what to review.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Icons | Lucide React |
| Backend | Python, FastAPI |
| AI | OpenAI Agents SDK |
| Validation | Pydantic |
| Database | SQLAlchemy |
| PDF Processing | PyMuPDF |
| Embeddings | OpenAI Embeddings / Local Demo Embeddings |
| Vector Search | FAISS |

## Project Structure

```text
ExamPilot/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docs/
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Prerequisites

Install the following:

- Python 3.11 or newer
- Node.js and npm
- Git

Verify your installations:

```powershell
python --version
node --version
npm --version
git --version
```

## Installation and Setup

### 1. Clone the repository

```powershell
git clone <REPOSITORY_URL>
cd ExamPilot
```

If you already have the project, simply open a terminal in its root directory.

### 2. Set up the Python virtual environment

From the project root:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your terminal should now show `(.venv)`.

### 3. Install backend dependencies

Make sure the virtual environment is activated.

```powershell
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend/` directory if you want to use the OpenAI API.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

MAX_UPLOAD_MB=30
```

**Important:**
- Replace the API key with your own key.
- Never commit `.env` or expose API keys in frontend code.
- Without an API key, the backend can use its local demo embedding and course-analysis fallback.
- Demo mode is useful for development, but it is not equivalent to full AI functionality.

### 5. Install frontend dependencies

Open a second PowerShell terminal:

```powershell
cd ExamPilot\frontend
npm install
```

If you are already in the project root:

```powershell
cd frontend
npm install
```

## Running ExamPilot

ExamPilot requires two terminals: one for the backend and another for the frontend.

### Terminal 1 — Backend

From the project root:

```powershell
cd backend
```

Activate the virtual environment if it is not already active:

```powershell
..\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

If activation does not work, invoke the virtual environment's Python directly:

```powershell
& "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

### Terminal 2 — Frontend

From the project root:

```powershell
cd frontend
```

Start the Vite development server:

```powershell
npm run dev
```

Frontend URL:

http://localhost:5173

Keep both terminals running while using ExamPilot.

## Available API Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| POST | `/api/courses/upload` | Upload and analyze PDFs |
| GET | `/api/courses` | List courses |
| GET | `/api/courses/{cid}` | Get course details |
| GET | `/api/courses/{cid}/knowledge-map` | Get course knowledge map |
| DELETE | `/api/courses/{cid}` | Delete a course |
| POST | `/api/courses/{cid}/diagnostic` | Start a diagnostic |
| GET | `/api/diagnostics/{did}` | Get diagnostic |
| POST | `/api/diagnostics/{did}/answer` | Submit a diagnostic answer |
| GET | `/api/diagnostics/{did}/results` | Get diagnostic results |
| POST | `/api/teaching-sessions` | Create a teaching session |
| GET | `/api/teaching-sessions/{sid}` | Get teaching session |
| POST | `/api/teaching-sessions/{sid}/advance` | Advance teaching stage |
| POST | `/api/teaching-sessions/{sid}/check` | Check a student answer |
| POST | `/api/exams/course/{cid}` | Generate an exam |
| GET | `/api/exams/{eid}` | Get an exam |
| POST | `/api/exams/{eid}/submit` | Submit an exam |
| GET | `/api/exams/{eid}/results` | Get exam results |
| GET | `/api/dashboard` | Get dashboard data |

For interactive API testing, use the Swagger documentation at `/docs`.

## Building the Frontend

To check the production build:

```powershell
cd frontend
npm run build
```

To preview the production build:

```powershell
npm run preview
```

## Testing Workflow

To test the complete student journey:

1. Start the backend and frontend.
2. Open ExamPilot in your browser.
3. Upload a text-based PDF course.
4. Verify that the course is extracted and analyzed.
5. Inspect the generated knowledge map.
6. Start a diagnostic and answer the questions.
7. Review the diagnostic results.
8. Start a personalized teaching session.
9. Complete the teaching stages and verification questions.
10. Generate and submit a practice exam.
11. Review the exam results and dashboard.

### PDF Requirements

- Only PDF files are accepted.
- Multiple PDFs can be uploaded together.
- Maximum file size: 30 MB per file.
- PDFs must contain extractable text.
- Scanned PDFs requiring OCR are not currently supported.

## Development Notes

- Keep API keys on the backend.
- Use the virtual environment for all Python commands.
- Run npm commands from the `frontend/` directory.
- Keep API routes focused on HTTP handling.
- Put business logic in backend services.
- Validate structured AI outputs.
- Keep grading deterministic on the backend.
- Use course content as the primary source for generated learning material.

## Troubleshooting

### `ModuleNotFoundError: No module named 'sqlalchemy'`

The wrong Python interpreter may be running.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or run Python directly:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
```

### `ModuleNotFoundError: No module named 'app'`

Make sure your terminal is inside the `backend/` directory before running Uvicorn.

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

### `npm error Missing script: "dev"`

Make sure you are inside `frontend/`, not the project root or `backend/`.

```powershell
cd frontend
npm run dev
```

### Port already in use

Stop the previous server with `Ctrl + C` before restarting it.

### PDF upload errors

Check that the file is a valid, text-based PDF and does not exceed the configured upload limit. Check the backend terminal for the corresponding error.

---

**ExamPilot — Understand your course. Discover your weaknesses. Improve your learning.**