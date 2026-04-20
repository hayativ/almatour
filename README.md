# Almatour

Interactive tourism guide for Almaty, Kazakhstan. Built with Django REST Framework + React (Vite).

---

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
  - [Prerequisites](#prerequisites)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Configure environment variables](#2-configure-environment-variables)
  - [3. Build and start the stack](#3-build-and-start-the-stack)
  - [4. Create a superuser](#4-create-a-superuser)
  - [Useful commands](#useful-commands)
  - [Architecture](#architecture)
- [API Documentation](#api-documentation)

---

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt
PROJECT_ENV_ID=local python manage.py migrate
PROJECT_ENV_ID=local python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` and `/media` requests to `http://localhost:8000`, so both services can run simultaneously without CORS issues.

---

## Production Deployment

### Prerequisites

- Docker ≥ 24 and Docker Compose plugin (`docker compose`)
- A Linux server with port 80 (and optionally 443) open

### 1. Clone the repository

```bash
git clone <repo-url> almatour
cd almatour
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set every value:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Long random Django secret key |
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of domains/IPs, e.g. `example.com,www.example.com` |

Generate a secure `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Build and start the stack

```bash
docker compose up -d --build
```

This will:
1. Build the backend image — installs Python dependencies, then the entrypoint runs `migrate`, `collectstatic`, and starts Gunicorn. Data is stored in an SQLite database persisted via a Docker volume.
2. Build the frontend image — compiles the React app with Vite, then serves it via nginx.

Check that both containers are healthy:

```bash
docker compose ps
```

The application is now available at `http://<your-server-ip>/`.

### 4. Create a superuser

```bash
docker compose exec backend python manage.py createsuperuser
```

The Django admin panel is at `/admin/`.

---

### Useful commands

```bash
# View live logs
docker compose logs -f

# View logs for a single service
docker compose logs -f backend

# Restart a single service (e.g. after changing .env)
docker compose restart backend

# Apply new migrations after a code update
docker compose exec backend python manage.py migrate

# Pull latest code and redeploy
git pull
docker compose up -d --build

# Stop all services
docker compose down

# Stop and delete volumes (WARNING: deletes the database and all uploads)
docker compose down -v
```

---

### CI/CD

The project uses GitHub Actions for automated deployment. On every push to `main`, the workflow in `.github/workflows/deploy.yml`:

1. SSHs into the production server.
2. Pulls the latest code from `main`.
3. Verifies the `.env` file exists.
4. Rebuilds and restarts the Docker containers.
5. Prunes unused Docker images.

Required GitHub secrets:

| Secret | Description |
|---|---|
| `SERVER_HOST` | IP or hostname of the production server |
| `SERVER_USER` | SSH username |
| `SSH_PRIVATE_KEY` | Private key for SSH authentication |
| `SERVER_PORT` | SSH port (defaults to 22) |
| `DEPLOY_PATH` | Absolute path to the project on the server |

---

### Architecture

```
Browser (port 80)
    │
    ▼
nginx (frontend container)
    ├── /static/*  ──► shared volume (populated by collectstatic)
    ├── /media/*   ──► shared volume (user-uploaded files)
    ├── /api/*     ──► backend:8000 (Gunicorn)
    ├── /admin/*   ──► backend:8000 (Gunicorn)
    └── /*         ──► React SPA (index.html)

backend container
    ├── Gunicorn → Django (settings.env.prod)
    └── SQLite database (persisted via sqlite_data volume)
```

Static and media files are shared between `backend` and `frontend` via named Docker volumes (`static_data`, `media_data`), so nginx serves them directly without going through Gunicorn. The SQLite database is persisted in a separate `sqlite_data` volume mounted at `/app/data/`.

---

## API Documentation

Swagger UI is available at `/api/v1/schema/swagger-ui/` (accessible only when `DEBUG=True` or when the schema endpoint is explicitly enabled).