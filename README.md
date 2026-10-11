# Psyche Research Engine

Psyche is a research workspace for discovering psychological literature, organizing projects, and saving papers from OpenAlex.

## V1 scope

- Clerk-authenticated workspace.
- Create, list, view, update, and delete research projects.
- Search OpenAlex works with publication-type and publication-date filters.
- Save, list, and remove papers in a project.
- Persistent storage in Supabase Postgres.

## Architecture

- `frontend/`: Next.js, React, Clerk, and TypeScript.
- `backend/`: FastAPI, Clerk Backend SDK, Supabase Python client, and OpenAlex API integration.
- `backend/migrations/`: SQL schema migrations. Apply them in numeric order in your Supabase project.

The frontend calls the FastAPI backend. The backend uses the Supabase service-role key; never expose that key to the browser. Clerk webhooks synchronize user records into the `users` table. Delivery IDs are persisted in `clerk_webhook_events` to make webhook retries idempotent.

## Local development

### 1. Configure environment

Copy `backend/.env.example` to `backend/.env` and `frontend/.env.example` to `frontend/.env.local`. Replace placeholders with values from your Supabase and Clerk projects. Configure an OpenAlex API key for authenticated OpenAlex requests.

### 2. Apply database migrations

Apply the SQL files in `backend/migrations/` in order, including migration 008 for Clerk webhook deduplication. The RLS hardening migration enables row-level security and revokes direct table privileges from Supabase `anon` and `authenticated` roles because access is routed through FastAPI using the service role. Verify the service-role key is configured only on the backend.

### 3. Start the backend

From the repository root:

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs are available at `http://localhost:8000/docs`.

### 4. Start the frontend

In a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

### 5. Configure Clerk webhooks

In the Clerk dashboard, create a webhook targeting `https://YOUR_BACKEND_HOST/api/webhooks/clerk`. Subscribe to `user.created`, `user.updated`, and `user.deleted`, then place its signing secret in `CLERK_WEBHOOK_SIGNING_SECRET`. For local webhook development, use Clerk's supported forwarding tool and its generated signing secret.

## Tests and quality checks

Backend tests use placeholder environment values and mock external service calls:

```bash
cd backend
python -m pip install -r requirements-dev.txt
python -m pytest --cov=app --cov-report=term-missing
```

Frontend checks:

```bash
cd frontend
npm ci
npm run lint
npx tsc --noEmit
npm run build
```

GitHub Actions runs these checks for pull requests to `main`.

## Production checklist

- Set `CORS_ALLOWED_ORIGINS` to exact deployed frontend origin(s), comma-separated.
- Set `CLERK_AUTHORIZED_PARTIES` to trusted frontend origin(s), comma-separated.
- Configure backend secrets in the hosting provider; do not commit real `.env` files.
- Configure Clerk's webhook URL and signing secret for the deployed backend.
- Apply all migrations, then verify RLS and table grants in the actual Supabase project.
- Confirm the deployed backend can reach Supabase and OpenAlex.
- Run the end-to-end flow: sign up → create project → search papers → save → reload → remove → verify another user cannot access the project.
- Verify responsive layout and navigation on desktop and mobile.

Repository CI cannot verify production secrets, live Supabase RLS/grants, Clerk dashboard settings, or the full deployed user journey. Those require checks against the configured services.
