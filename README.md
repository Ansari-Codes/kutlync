# KutLynk

This REPO contains:

- frontend: Vue 3 + Vite app
- backend: FastAPI (Python) + SQLite app

## Backend

Install dependencies:

```bash
cd backend-fastapi
pip install -r requirements.txt
uvicorn Main:app --reload --host 127.0.0.1 --port 3333
```

Local API base:

```text
http://127.0.0.1:3333
```

## Frontend

Install dependencies:

```bash
cd frontend
npm install
npm run dev
```

The frontend uses the Vite dev host from `vite.config.ts` for API calls, and backend runs on a separate port (`3333` here).