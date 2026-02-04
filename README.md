
# Intern Management (Django + DRF)

An Intern Management REST API built with **Django REST Framework**. It provides:

- User registration with roles (**INTERN** / **SUPERVISOR**)
- JWT authentication (access + refresh), plus sign-out via refresh token blacklisting
- Task management (CRUD) with a "complete" action
- Daily attendance marking (max 1 record per user per date)
- Interactive API docs via Swagger UI and ReDoc

---

## Tech stack

- Python + Django
- Django REST Framework (DRF)
- SimpleJWT (`rest_framework_simplejwt`) + token blacklisting
- `drf_yasg` for Swagger / ReDoc
- `django-filter` for filtering
- SQLite (default, `db.sqlite3`)

---

## Project structure

- Django project: `Project/`
	- Settings: `Project/settings.py`
	- Root URLs: `Project/urls.py`
- App: `intern/`
	- Models: `intern/models.py`
	- Serializers: `intern/serializers.py`
	- Permissions: `intern/permissions.py`
	- Views: `intern/views.py`
	- Routes: `intern/urls.py`
- Entry point: `manage.py`

---

## Roles and permissions

Roles are stored in `intern.models.UserProfile` and created during registration.

Valid roles:

- `INTERN`
- `SUPERVISOR`

Task create/update/delete is restricted to supervisors via `intern.permissions.IsSupervisor`.

---

## Authentication (JWT)

JWT is configured in `Project/settings.py` under `REST_FRAMEWORK` and `SIMPLE_JWT`.

Configured lifetimes:

- Access token: 5 minutes
- Refresh token: 1 day

Sign-in returns both tokens. Sign-out blacklists the refresh token (requires `rest_framework_simplejwt.token_blacklist` in `INSTALLED_APPS`).

---

## Data model (summary)

Defined in `intern/models.py`.

### UserProfile

- `user`: OneToOne to Django `auth.User`
- `role`: `INTERN` or `SUPERVISOR`

### Task

- `title`: text
- `assigned_to`: ForeignKey to `auth.User`
- `status`: `PEND` (pending) or `COMP` (completed)
- `created_at`: created timestamp
- `completed_at`: completion timestamp

### Attendence

- `user`: ForeignKey to `auth.User`
- `date`: DateField

Uniqueness rule:

- `(user, date)` must be unique (prevents multiple attendance entries per day)

---

## API documentation

Routes are defined in `Project/urls.py`.

- Swagger UI: `GET /swagger/`
- ReDoc: `GET /redoc/`

---

## API endpoints

App endpoints are mounted under `/app/` in `Project/urls.py` and implemented in `intern/`.

### Auth / user

- `POST /app/user_register/`
	- Creates a Django `User` and a `UserProfile` with role
	- Implemented by `intern.views.user_register`

- `POST /app/sign_in/`
	- Returns `{ refresh, access, user }`
	- Implemented by `intern.views.SignInView`

- `POST /app/sign_out/`
	- Blacklists the provided refresh token
	- Implemented by `intern.views.SignOutView`

- `POST /api/token/refresh/`
	- Standard SimpleJWT refresh endpoint

### Attendance

- `POST /app/mark_attendence/`
	- Marks attendance for the authenticated user for today
	- One record per day per user
	- Implemented by `intern.views.mark_attendence`

### Tasks (ViewSet)

Implemented in `intern.views.TaskViewSet` and registered by router in `intern/urls.py`.

Common routes:

- `GET /app/tasks/` (list)
- `POST /app/tasks/` (create; supervisor-only)
- `GET /app/tasks/{id}/` (retrieve)
- `PUT/PATCH /app/tasks/{id}/` (update; supervisor-only)
- `DELETE /app/tasks/{id}/` (delete; supervisor-only)
- `POST /app/tasks/{id}/complete/` (complete; only assigned user)
- `PATCH /app/tasks/{id}/soft_delete` (soft_delete: supervisor-only)
- `POST /app/tasks/{id}/restore` (restore task: supervisor-only)

---

## Filtering / search / ordering (tasks)

Configured in `intern.views.TaskViewSet`.

Examples:

- Filter by assigned user: `GET /app/tasks/?assigned_to__username=alice`
- Filter by status: `GET /app/tasks/?status=COMP`
- Search by title: `GET /app/tasks/?search=report`
- Order by creation time: `GET /app/tasks/?ordering=-created_at`

---

## Local setup (development)

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 2) Install dependencies

If you don’t have a `requirements.txt` yet, install the known dependencies:

```bash
pip install Django djangorestframework djangorestframework-simplejwt drf-yasg django-filter
```

### 3) Apply migrations

```bash
python manage.py migrate
```

### 4) Run the server

```bash
python manage.py runserver
```

Open:

- API docs: `http://127.0.0.1:8000/swagger/`
- Admin: `http://127.0.0.1:8000/admin/`

---

## Example requests (cURL)

### Register a user

```bash
curl -X POST http://127.0.0.1:8000/app/user_register/ \
	-H "Content-Type: application/json" \
	-d '{"username":"alice","password":"pass1234","role":"INTERN"}'
```

### Sign in (get JWT tokens)

```bash
curl -X POST http://127.0.0.1:8000/app/sign_in/ \
	-H "Content-Type: application/json" \
	-d '{"username":"alice","password":"pass1234"}'
```

### Mark attendance (requires access token)

```bash
curl -X POST http://127.0.0.1:8000/app/mark_attendence/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Create a task (supervisor-only)

`assigned_to` uses the user’s username.

```bash
curl -X POST http://127.0.0.1:8000/app/tasks/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>" \
	-H "Content-Type: application/json" \
	-d '{"title":"Write weekly report","assigned_to":"alice","status":"PEND"}'
```

### Complete a task (only the assigned user)

```bash
curl -X POST http://127.0.0.1:8000/app/tasks/1/complete/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Sign out (blacklist refresh token)

```bash
curl -X POST http://127.0.0.1:8000/app/sign_out/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>" \
	-H "Content-Type: application/json" \
	-d '{"refresh":"<REFRESH_TOKEN>"}'
```

---

## Admin

Models are registered in `intern/admin.py`.

Create an admin user:

```bash
python manage.py createsuperuser
```

Then visit: `http://127.0.0.1:8000/admin/`

---



