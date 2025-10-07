# SnippetShare

A minimal snippet sharing web app (Flask + SQLite) — save, view and share text snippets.

Author / Copyright: Jeevan Rao

---

## Quick overview
- Single-file Flask backend + static frontend
- SQLite DB (schema.sql) for snippet storage
- REST API: GET /api/snippets, GET /api/snippets/:id, POST /api/snippets, PUT /api/snippets/:id, DELETE /api/snippets/:id
- UI supports creating, editing (updates create a new revision), searching, copying and sharing snippets

---


## Local development (macOS)

1. Clone repo and cd into project
2. Create & activate virtualenv:
   - python3 -m venv .venv
   - source .venv/bin/activate
3. Install dependencies:
   - pip install -r requirements.txt
4. Initialize database (one-time):
   - export FLASK_APP=app
   - flask --app app init-db
   This creates `snippets.db` using `schema.sql`.
5. Run dev server:
   - python app.py
   - or: FLASK_APP=app FLASK_ENV=development flask run --host=0.0.0.0 --port=8000

Open http://localhost:8000

Notes:
- Set environment variables (SECRET_KEY, DATABASE) as needed.
- If `requirements.txt` is missing, use `pip install flask`.

---

## Roadmap

Planned improvements / milestones:
- UX / UI
  - Dark/light theme toggle
  - Autosave with configurable interval (current implementation supports autosave)
  - Inline editing and revision history
  - Keyboard shortcuts (Ctrl/Cmd+S to save; Esc to clear)
- API & backend
  - Pagination for GET /api/snippets
  - Authentication & per-user snippets (JWT or OAuth)
  - Rate limiting and size limits for content
  - Switchable DB adapters (Postgres/MariaDB) for production
- Devops / infra
  - Dockerfile + docker-compose for local dev
  - CI (tests, lint) and automated deployments
  - Systemd / Gunicorn production example
- Analytics & moderation
  - Basic analytics (views, shares)
  - Moderation tools, spam prevention
- Tests
  - Unit tests for API endpoints
  - End-to-end tests for critical flows (save, share, load)

Contributions welcome — open an issue or PR.

---

## Production deployment (suggestions)

Use Gunicorn behind nginx. Example:

- pip install gunicorn
- gunicorn --workers 3 --bind 0.0.0.0:8000 "app:app"

Set environment variables:
- SECRET_KEY — replace default value
- DATABASE — path to sqlite file or DB URL for production

Notes:
- SQLite is simple but not ideal for high concurrency — consider PostgreSQL for production.
- Ensure file permissions on the sqlite DB allow the web server user to read/write.

Optional Docker (quick example)
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=app
RUN flask --app app init-db
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

---

## API

- GET /api/snippets
  - Returns: JSON array of snippets (id, content, created_at)
  - Optional: add pagination in future
- GET /api/snippets/<id>
  - Returns: JSON object for snippet or 404
- POST /api/snippets
  - Body: { "content": "your text" }
  - Returns: { "id": <newId>, "message": "Snippet created successfully" }
- PUT /api/snippets/<id>
  - Body: { "content": "updated text" }
  - Returns: 200 OK and updated snippet
- DELETE /api/snippets/<id>
  - Returns: 204 No Content on success

---

## Security & notes
- Replace `app.config['SECRET_KEY']` with a secure value in production (use env var).
- Sanitize or limit snippet size when allowing public uploads.
- Consider rate-limiting to prevent abuse.

---

If you want, I can:
- Add screenshot placeholders into `screenshots/`
- Add Docker Compose and systemd examples
- Add API unit tests and basic CI config