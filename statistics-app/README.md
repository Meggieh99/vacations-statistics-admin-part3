# Vacation Management System – Part III

A Dockerized system composed of four services sharing the same PostgreSQL database:

* **vacations** – Django app for users (list/like/unlike, details, admin CRUD pages).
* **backend** – Django API for the statistics dashboard.
* **frontend** – React app for the statistics dashboard.
* **database** – PostgreSQL 16 with initial seed data.

The two web apps read/write the **same DB**, so actions like “like” in the vacations app are reflected immediately in the statistics app.

---

## Project structure

```
stats_backend/
├─ docker-compose.yml
├─ init/
│  └ init.sql                     # initial schema/data (runs only on first DB volume creation)
├─ vacations/                      # Django app (user-facing Vacations)
│  ├─ vacations_backend/           # settings/urls/wsgi
│  └─ templates/                   # HTML pages
├─ stats_backend/                  # Django API for statistics
│  └─ stats_api/
└─ statistics-app/                 # React dashboard (admin)
   ├─ src/
   ├─ package.json
   └─ Dockerfile
```

---

## Services & Ports

* Vacations (Django): `http://localhost:8000`
* Statistics API (Django): `http://localhost:9000`
* Statistics UI (React): `http://localhost:3000`
* PostgreSQL: `localhost:5432`

---

## Statistics Dashboard (Implemented)

* **Total likes** KPI.
* **Filters**: minimum likes, “destination contains”.
* **Charts**:

  * Likes per destination (bar chart).
  * Likes share (donut/pie).
* **Session-aware endpoints** (login/logout/session) used by the dashboard.

API paths used by the frontend:

```
POST  /api/login/
POST  /api/logout/
GET   /api/session/
GET   /api/vacations/stats/        # aggregates for the dashboard
GET   /api/users/total/
GET   /api/likes/total/
GET   /api/likes/distribution/
```

Note: both apps share the same Postgres DB, so likes from the Vacations app are visible in these aggregates.

---

## Prerequisites

* Docker Desktop (includes Docker Compose)
* Git
* Optional: Docker Hub account (to pull prebuilt images)

---

## Run locally with Compose

From the project root:

```
docker compose up --build
```

First run creates the DB volume and executes `init/init.sql`.
Subsequent runs reuse the volume (no re-seeding).

Open:

* Vacations app: `http://localhost:8000`
* Statistics UI: `http://localhost:3000`

---

## Initial Data and DB Notes

* `init/init.sql` runs **only** when the Postgres volume is created the first time.
* To re-seed from scratch (**deletes all data**):

```
docker compose down -v
docker compose up --build
```

---

## Tests

Frontend (React) tests:

```
cd statistics-app
npm test
```

> Django tests are not required for this submission; only frontend tests are included.

---

## Docker Hub (Prebuilt Images)

If you prefer to pull instead of building locally:

```
docker pull meggie87/vacations:latest
docker pull meggie87/stats-backend:latest
docker pull meggie87/stats-frontend:latest
```

Update `docker-compose.yml` to use `image:` instead of `build:` for each service.

---

## Deployment on AWS (EC2 Quick Path)

1. Launch an Ubuntu EC2 instance and open security-group ports 80/443 (and 3000/8000/9000 for testing if needed).
2. SSH to the instance and install Docker + Docker Compose.
3. `git clone` this repository on the server.
4. `docker login` (if pulling from Docker Hub).
5. `docker compose up -d` to run in background.

Production tips:

* Set `ALLOWED_HOSTS` in both Django settings.
* Use a reverse proxy (e.g., Nginx) to expose a single domain.
* Add environment variables via compose or `.env` file (DB creds already passed in compose).

---

## Credentials (To Fill)

Provide demo credentials for grading:

```
Admin email: <fill-in>
Password:    <fill-in>
```

---

## Common Issues

* **Like/unlike returns 404**: make sure the frontend endpoints include the `/api/` prefix and match the Django `urls.py`.
* **init.sql didn’t run again**: remove the DB volume (`docker compose down -v`) if you truly need a clean seed.
* **Static/UI looks off in Django pages**: ensure static files are copied into the image and `STATIC_URL` / `collectstatic` are configured if you serve Django templates in production.

---

## License

Educational project for the Full-Stack Python course.

---

### You Still Need to Fill In:

* [ ] Admin credentials (`email`/`password`) for testing.
* [ ] Add screenshots of your final UI.
* [ ] Add your GitHub repository link (optional).
* [ ] Add your AWS deployment link (if applicable).
* [ ] Optional: add a short video demo or recording.


Author
Meggie Hadad GitHub: meggie87
