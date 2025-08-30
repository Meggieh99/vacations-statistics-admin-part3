# Vacation Management System – Part III


A full-stack Dockerized system that allows users to browse, like, and manage vacation destinations, while administrators can monitor statistics in a dedicated dashboard. The system is composed of two Django apps (user-facing and API), one React app for analytics, and a shared PostgreSQL database. All services are containerized and connected via Docker Compose.
A Dockerized system composed of four services sharing the same PostgreSQL database:


- **vacations** – Django app for users (list/like/unlike, details, admin CRUD pages).
- **backend** – Django API for the statistics dashboard.
- **frontend** – React app for the statistics dashboard.
- **database** – PostgreSQL 16 with initial seed data.

Both web apps read/write the **same DB**, so actions like "like" in the vacations app are reflected immediately in the statistics app.

---

## Project Structure

```
stats_backend/
├─ docker-compose.yml
├─ init/
│  └ init.sql                     # initial schema/data (runs only on first DB volume creation)
├─ vacations/                      # Django app (user-facing Vacations)
│  ├ vacations_backend/           # settings/urls/wsgi
│  └ templates/                   # HTML pages
├─ stats_backend/                  # Django API for statistics
│  └ stats_api/
└ statistics-app/                 # React dashboard (admin)
   ├ src/
   ├ package.json
   └ Dockerfile
```

---

## Services & Ports

- Vacations (Django): `http://localhost:8000`
- Statistics API (Django): `http://localhost:9000`
- Statistics UI (React): `http://localhost:3000`
- PostgreSQL: `localhost:5432`

---

## Statistics Dashboard (Implemented)

- **Total likes** KPI
- **Filters**: minimum likes, “destination contains”
- **Charts**:
  - Likes per destination (bar chart)
  - Likes share (donut/pie)
- **Session-aware endpoints** (login/logout/session) used by the dashboard

API paths used by the frontend:

```
POST  /api/login/
POST  /api/logout/
GET   /api/session/
GET   /api/vacations/stats/
GET   /api/users/total/
GET   /api/likes/total/
GET   /api/likes/distribution/
```

---

## Prerequisites

- Docker Desktop (includes Docker Compose)
- Git
- Optional: Docker Hub account (to pull prebuilt images)

---

## Docker Compose Configurations

This project includes three Docker Compose files to support different environments:

- **`docker-compose.dev.yml`** – Full development setup. Builds all images locally, mounts source files for live changes.
  ```bash
  docker compose -f docker-compose.dev.yml up --build
  ```

- **`docker-compose.prod.yml`** – Production-ready setup for servers (e.g., EC2). Uses prebuilt images from Docker Hub.
  ```bash
  docker compose -f docker-compose.prod.yml up -d
  ```

- **`docker-compose.mini.yml`** – Minimal setup to test critical services (e.g., backend + DB) without loading the full stack.
  ```bash
  docker compose -f docker-compose.mini.yml up --build
  ```

---

## Initial Data and DB Notes

- `init/init.sql` runs **only** when the Postgres volume is created the first time.
- To re-seed from scratch (**deletes all data**):

```bash
docker compose down -v
docker compose up --build
```

---

## Frontend Tests

```bash
cd statistics-app
npm test
```

> Django tests are not required for this submission; only frontend tests are included.

---

## Docker Hub (Prebuilt Images)

If you prefer to pull instead of building locally:

```bash
docker pull meggie87/stats-frontend:v5
docker pull meggie87/stats-backend:v4
docker pull meggie87/vacations:v3
```

Update `docker-compose.yml` to use `image:` instead of `build:` for each service.

---

## EC2 Deployment Notes

1. Launch an EC2 instance (Ubuntu).
2. Open ports: 3000, 8000, 9000 (inbound rules).
3. Install Docker & Docker Compose.
4. Clone project + pull images.
5. Run with:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Production tips:
- Set `ALLOWED_HOSTS` in Django settings.
- Use a reverse proxy (e.g., Nginx) to expose a single domain.
- Add environment variables via compose or `.env` file (DB creds already passed in compose).

---

## Common Issues

- **React 404 / failed proxy** – happens when backend isn’t running or not reachable from frontend.
- **init.sql didn't re-run** – delete volumes using `docker compose down -v`.
- **Missing recharts module** – ensure it exists in `package.json`, then rebuild the image.

---

## Test Admin Credentials

```text
Email:    admin@admin.com
Password: adminadmin
```

---

## License

Educational project for the Full-Stack Python course.

GitHub: https://github.com/Meggieh99/vacations-statistics-admin-part3

Author: Meggie Hadad

