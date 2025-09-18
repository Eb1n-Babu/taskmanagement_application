**Task Management Application with Task Completion Report**

**Project Status
Note: This project is still under active development as of September 18, 2025. 
Some features and functions may not work properly or could be incomplete. Please report 
any issues via GitHub, and feel free to contribute to improve it.**

`Overview`
This project enhances a Task Management Application by incorporating features for users to submit completion reports 
and worked hours when marking tasks as completed. It promotes transparency and accountability in task tracking.
The application includes a RESTful API with JWT authentication for user interactions and a custom Admin Panel 
built with HTML templates for Admin and SuperAdmin roles to manage users, admins, tasks, and reports.
Developed using Python and Django, the system defines clear roles (SuperAdmin, Admin, User) with specific permissions.
API endpoints are created for task management and reporting (without full integration), and the Admin Panel provides
a web interface for oversight. The database uses SQLite, and validations ensure that completion reports and positive
worked hours are mandatory for completed tasks.

**Features**

**Roles and Permissions:**

SuperAdmin: Full access to manage admins (create, delete, assign roles, promote/demote), users (create, delete, update), 
assign users to admins, view/manage all tasks, and view task reports.
Admin: Manage tasks for their assigned users (create, assign, view, update), view completion reports and worked hours, 
but cannot manage user roles.
User: View assigned tasks, update task status (including marking as completed with required report and hours), interact 
only via API for their own tasks.


**Task Management:**

Create, assign, update, and view tasks with fields like title, description, assigned_to, due_date, status (Pending, 
In Progress, Completed), completion_report, and worked_hours.
Mandatory completion report (brief description of work done, challenges, etc.) and worked hours (positive numeric value) 
when marking tasks as completed.
Admins/SuperAdmins can review reports for completed tasks.


**API Endpoints:**

Secure JWT authentication for user access.
Task listing, updating (with validations), and report viewing.


**Admin Panel:**

Custom web interface using HTML templates for SuperAdmin and Admin features.
Views for managing users, admins, tasks, and reports.


**Security and Validations:**

JWT for API authentication.
Role-based access control.
Validations to enforce report and hours on completion; restrict user interactions to own tasks.


**Technologies Used**

Backend: Python 3.8+, Django 4.x, Django REST Framework (DRF) 3.14+.
Authentication: django-rest-framework-simplejwt for JWT.
Frontend: HTML5 with custom templates (Bootstrap optional for styling).
Database: SQLite (as specified).
Other: Standard Django tools for migrations and admin.

**Installation
Prerequisites**

Python 3.8 or higher.
Virtual environment tool (e.g., venv).
Git (for cloning).

**Steps**

**Clone the Repository:**
git clone https://github.com/Eb1n-Babu/taskmanagement_application.git
cd task-management-app

**Set Up Virtual Environment:**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install Dependencies:**
The requirements.txt includes:
django>=4.0
djangorestframework>=3.14
djangorestframework-simplejwt>=5.2

**Run:**
pip install -r requirements.txt

**Database Setup:**
Using SQLite (no external setup needed):
python manage.py makemigrations
python manage.py migrate

**Create Superuser (SuperAdmin):**
python manage.py createsuperuser
This creates a SuperAdmin account for initial access.
* superadmin/superpass → default for all API tests, email- superadmin@gmail.com

**Run the Server:**
python manage.py runserver

Access the API at http://127.0.0.1:8000/api/ and Admin Panel at http://127.0.0.1:8000/admin-panel/ (adjust paths based on urls.py).

**Project Structure**

taskmanagement/                  # Project root
├── .gitignore                   # Git ignore file
├── README.md                    # Project documentation
├── manage.py                    # Django management script
├── requirements.txt             # Dependencies
├── db.sqlite3                   # SQLite DB (generated after migrate)
├── taskmanagement/              # Project settings
│   ├── __init__.py
│   ├── asgi.py                  # ASGI config (default)
│   ├── settings.py              # Settings (updated)
│   ├── urls.py                  # Main URLs (updated)
│   └── wsgi.py                  # WSGI config (default)
├── taskmanager/                 # Single Django app
│   ├── __init__.py
│   ├── admin.py                 # Django admin (basic)
│   ├── apps.py                  # App config (default)
│   ├── forms.py                 # Web forms
│   ├── migrations/              # DB migrations (generated)
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py                # Models (Task)
│   ├── permissions.py           # Custom DRF permissions
│   ├── serializers.py           # DRF serializers
│   ├── tests.py                 # Test cases (new)
│   ├── urls.py                  # App URLs (optional, not used here)
│   └── views.py                 # API + Web views
├── templates/                   # Custom HTML templates
│   └── admin_panel/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── users/
│       │   ├── list.html
│       │   ├── form.html
│       │   └── role_form.html
│       ├── admins/
│       │   └── list.html
│       └── tasks/
│           ├── list.html
│           ├── form.html
│           └── detail.html
└── static/                      # Static files (empty for now, add CSS/JS if needed)
    └── admin_panel/             # Optional: CSS for panel


📌 TaskManager – auto Testing 

⚡ How to Run the Tests

1. Make sure your virtual environment is activated and dependencies installed.

**pip install -r requirements.txt**

2. Run the test suite with:

**python manage.py test**

3. (Optional) To see more detailed output:

**python manage.py test -v 2**

✅ Django will automatically discover all tests inside your app (tests.py or tests/ package).
✅ These tests cover models, serializers, APIs, and admin panel workflows.

📌 TaskManager – Manual Testing (Postman)

This project is a Django + DRF Task Management System with role-based access control:
* SuperAdmin → Full system control
* Admin → Limited (manage tasks, not users)
* User → Only own tasks

This guide provides setup and manual tests using Postman.

⚡ Always use:
* superadmin/superpass → default for all API tests
* testuser/testpass → only for “own tasks” tests

🚀 1. Setup Instructions
1.1 Apply Migrations
* python manage.py makemigrations taskmanager
* python manage.py migrate
1.2 Create SuperAdmin
* python manage.py createsuperuser

Username: superadmin
email:superadmin@gmail.com
Password: superpass

1.3 Assign Role
Go to /admin/
Navigate: Groups → SuperAdmin → Add superadmin

1.4 (Optional) Seed Test User
* python manage.py shell
```
from django.contrib.auth.models import User, Group
from taskmanager.models import Task
from datetime import date

Group.objects.get_or_create(name='User')[0]
Group.objects.get_or_create(name='Admin')[0]

testuser = User.objects.create_user(username='testuser', password='testpass', email='test@test.com')
testuser.groups.add(Group.objects.get(name='User'))

Task.objects.create(title='Test Task 1', description='Desc 1', assigned_to=testuser, due_date=date(2025, 10, 1), status='pending')
Task.objects.create(title='Test Task 2', description='Desc 2', assigned_to=testuser, due_date=date(2025, 10, 2), status='in_progress')

exit()
```

1.5 Run Server
* python manage.py runserver

🔑 2. Authentication (JWT) – Postman Tests

**| Test ID | Request                          | Body (JSON)                                           | Expected                                      |
| ------- | -------------------------------- | ----------------------------------------------------- | --------------------------------------------- |
| AUTH-01 | **POST** `/api/auth/login/`      | `{"username": "superadmin", "password": "superpass"}` | ✅ 200 OK, returns `access` + `refresh` tokens |
| AUTH-02 | **POST** `/api/auth/login/`      | `{"username": "superadmin", "password": "wrongpass"}` | ❌ 401 Unauthorized                            |
| AUTH-03 | **POST** `/api/auth/refresh/`    | `{"refresh": "<refresh_token>"}`                      | ✅ 200 OK, returns new `access`                |
| AUTH-04 | **GET** `/api/tasks/` (no token) | N/A                                                   | ❌ 401 Unauthorized                            |**

📌 Tip: In Postman, store access token in an environment variable {{super_token}}.     `#super_token == accees_token `

📌 3. Tasks API – Postman Tests

Headers for all requests:

* Authorization: Bearer {{super_token}}                                                 `#super_token == accees_token `
* Content-Type: application/json

**| Test ID | Request                                         | Body (JSON)                                                                | Expected                           |
| ------- | ----------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------- |
| TASK-01 | **GET** `/api/tasks/`                           | N/A                                                                        | ✅ 200 OK, list of tasks            |
| TASK-02 | **GET** `/api/tasks/` (as emptyuser)            | Login emptyuser, then GET                                                  | ✅ 200 OK, `[]`                     |
| TASK-03 | **PUT** `/api/tasks/1/`                         | `{"status": "completed", "completion_report": "Done.", "worked_hours": 5}` | ✅ 200 OK, task updated             |
| TASK-04 | **PUT** `/api/tasks/1/`                         | `{"status": "completed", "worked_hours": 5}`                               | ❌ 400 Bad Request (missing report) |
| TASK-05 | **PUT** `/api/tasks/1/`                         | `{"status": "completed", "completion_report": "Done", "worked_hours": 0}`  | ❌ 400 Bad Request (invalid hours)  |
| TASK-06 | **PUT** `/api/tasks/1/`                         | `{"status": "in_progress"}`                                                | ✅ 200 OK                           |
| TASK-07 | **PUT** `/api/tasks/<id>/` (testuser token)     | Update own task                                                            | ✅ 200 OK                           |
| TASK-08 | **GET** `/api/tasks/1/report/`                  | N/A                                                                        | ✅ 200 OK, report shown             |
| TASK-09 | **GET** `/api/tasks/1/report/` (testuser token) | N/A                                                                        | ❌ 403 Forbidden                    |
| TASK-10 | **GET** `/api/tasks/2/report/`                  | N/A                                                                        | ❌ 404 Not Found                    |**

🌐 4. Admin Panel (Browser Tests)

Open: http://127.0.0.1:8000/admin-panel/login/
**| Test ID  | Steps                                | Expected             |
| -------- | ------------------------------------ | -------------------- |
| PANEL-01 | Login `superadmin/superpass`         | Redirect → Dashboard |
| PANEL-02 | Login `adminuser/adminpass`          | Limited dashboard    |
| PANEL-03 | Login `testuser/testpass`            | ❌ Access denied      |
| PANEL-04 | As superadmin → `/users/` → CRUD     | ✅ Success            |
| PANEL-05 | `/admins/`                           | ✅ Shows admins       |
| PANEL-06 | `/tasks/` → Create task for testuser | ✅ Success            |
| PANEL-07 | Admin tries `/users/`                | ❌ 403 Forbidden      |
| PANEL-08 | Open completed task detail           | ✅ Report visible     |
| PANEL-09 | Logout                               | ✅ Redirect → Login   |**


🔐 5. Roles & Permissions

**| Test ID | Role                        | Expected               |
| ------- | --------------------------- | ---------------------- |
| ROLE-01 | Superadmin                  | Full access everywhere |
| ROLE-02 | Admin                       | ✅ Tasks, ❌ Users       |
| ROLE-03 | User                        | ❌ Panel access denied  |
| ROLE-04 | Superadmin API report       | ✅ 200                  |
| ROLE-05 | Promote/Demote in `/admin/` | Access changes         |**


🔄 6. Task Workflow

**| Test ID | Action                        | Expected                       |
| ------- | ----------------------------- | ------------------------------ |
| WF-01   | Create task (Panel)           | ✅ Saved as Pending             |
| WF-02   | Complete without report/hours | ❌ API 400 / Panel error        |
| WF-03   | Complete via API (valid)      | ✅ Task updated                 |
| WF-04   | View non-completed            | Message: “No report available” |
| WF-05   | Check in `/admin/`            | ✅ Data persists                |**

📂 Postman Setup

Instead of typing curl, follow this workflow:

1. Open Postman
2. Create a new Collection called TaskManager
3. Add folders: Auth, Tasks, Reports
4. Add each request above (method, URL, body)
5. Add environment variable:
   super_token → paste from AUTH-01 login response
   testuser_token → paste from testuser login

✅ Now you can run all API tests in Postman.
✅ Browser tests cover the panel features.

**Admin Panel**
Access via browser after login (implement custom login view).

**SuperAdmin:**
* Manage admins: Create, delete, assign roles, promote/demote.
* Manage users: Create, delete, update, assign to admins.
* View/manage all tasks and reports.

**Admin:**
* Assign tasks to their users.
* View/manage tasks for their users.
* View completion reports and worked hours.

Implement views with role checks (e.g., using decorators or middleware).

**Task Workflow**

1. SuperAdmin creates/admins users and assigns roles.
2. Admin assigns tasks to users.
3. User views tasks via API, updates to "Completed" with report/hours.
4. Admin/SuperAdmin reviews reports in panel or via API.

**Customization**

* Extend Models: Add custom User model for roles (e.g., using groups or custom fields).
* Permissions: Use DRF permissions and Django decorators for role-based access.
* Styling: Add Bootstrap/CDN to templates for responsive design.
* Deployment: For production, use Gunicorn/Nginx; secure settings (e.g., SECRET_KEY, disable debug).

**Contact**
[ebin.babu.in@icloud.com]

==========================================================Thanks=======================================================
Special thanks to GitHub for hosting the repository, YouTube for educational resources, and Grok for assistance in development.