# SmartDesk – IT Support Ticket Management System

# Day 1 – Project Setup & Database

### 1. Day 1 Objectives

The goal of Day 1 was to set up the development environment and build the basic structure of SmartDesk using Python, Flask, SQLite, HTML, and Git.

**Completed tasks:**
- Created the project folder.
- Set up Visual Studio Code.
- Created a Python virtual environment.
- Installed Flask.
- Created the Flask application.
- Created the SQLite database.
- Created the `users` and `tickets` tables.
- Added sample data for testing.
- Displayed tickets on the Dashboard.
- Created a GitHub repository and pushed the initial project.

---

### 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web framework |
| SQLite | Database |
| HTML | Website structure |
| Jinja2 | Display dynamic data in HTML |
| Git | Version control |
| GitHub | Store and manage project code |
| VS Code | Code editor |

---

### 3. Project Structure

Initial project structure:

```text
IT-Helpdesk-System/
├── .venv/
├── templates/
│   └── index.html
├── app.py
├── database.py
├── helpdesk.db
├── .gitignore
└── Note.md
```

**File explanations:**

- `app.py`: Runs the Flask application and handles routes.
- `database.py`: Creates the database and manages SQLite connections.
- `index.html`: Displays the SmartDesk Dashboard.
- `helpdesk.db`: Stores users and tickets.
- `.gitignore`: Prevents unnecessary or sensitive files from being uploaded to GitHub.
- `.venv`: Contains the Python virtual environment.

---

### 4. Python Virtual Environment

A virtual environment isolates project dependencies from other Python projects.

**Create a virtual environment:**

```powershell
python -m venv .venv
```

**Activate it in PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Install Flask:**

```powershell
pip install flask
```

**PowerShell issue encountered:**

PowerShell initially blocked script execution when activating the virtual environment.

**Solution used:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

This temporarily allows script execution for the current PowerShell session.

---

### 5. Flask Application

Flask is a Python web framework used to build web applications.

**Basic example:**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to SmartDesk"

if __name__ == "__main__":
    app.run(debug=True)
```

**Important concepts:**

- `Flask(__name__)`: Creates the Flask application.
- `@app.route("/")`: Defines the homepage URL.
- `def home()`: Function executed when the homepage is requested.
- `app.run(debug=True)`: Starts the Flask development server with debugging enabled.

**Run the application:**

```powershell
python app.py
```

**Local website:**

`http://127.0.0.1:5000/`

---

### 6. SQLite Database

SQLite is a lightweight database that stores data in a local file.

**Database file:** `helpdesk.db`

**Database connection:**

```python
import sqlite3

DB_NAME = "helpdesk.db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
```

**Explanation:**

- `sqlite3.connect()`: Opens the SQLite database.
- `sqlite3.Row`: Allows accessing database columns by name.
- `PRAGMA foreign_keys = ON`: Enables foreign key constraint enforcement.
- `connection.close()`: Closes the database connection.

---

### 7. Database Tables

**Users table:**

| Column | Description |
|---|---|
| id | Unique user ID |
| name | User's name |
| email | Unique email address |
| role | User role |

**Tickets table:**

| Column | Description |
|---|---|
| id | Unique ticket ID |
| title | Ticket title |
| description | Problem description |
| status | Current ticket status |
| priority | Ticket priority |
| user_id | ID of the user who created the ticket |
| created_at | Ticket creation timestamp |

**Important database concepts:**

- Primary Key: Uniquely identifies each record.
- Foreign Key: Creates a relationship between tables.
- `NOT NULL`: Requires a value.
- `UNIQUE`: Prevents duplicate values.
- `AUTOINCREMENT`: Automatically generates increasing IDs.
- `DEFAULT`: Provides a default value when none is supplied.

**Database relationship:**

One user can create multiple tickets.

`users.id` → `tickets.user_id`

---

### 8. Sample Data

During Day 1, two sample tickets were created to test the application.

**Ticket 1:**
- Title: Laptop cannot connect to Wi-Fi
- Description: Unable to connect to office Wi-Fi
- Status: Open
- Priority: High

**Ticket 2:**
- Title: Outlook not receiving emails
- Description: New emails are not appearing
- Status: In Progress
- Priority: Medium

A Demo User with `id = 1` was also created.

**Note:** The automatic sample-ticket insertion was removed during Day 2 to prevent deleted tickets from reappearing.

---

### 9. Displaying Tickets on the Dashboard

The homepage retrieves tickets from SQLite using a SQL query.

**Important SQL:**

```sql
SELECT tickets.id,
       tickets.title,
       tickets.description,
       tickets.status,
       tickets.priority,
       users.name AS created_by
FROM tickets
JOIN users ON tickets.user_id = users.id
ORDER BY tickets.id DESC
```

**Explanation:**

- `SELECT`: Retrieves data.
- `JOIN`: Combines data from the users and tickets tables.
- `AS created_by`: Assigns an alias to a column.
- `ORDER BY ... DESC`: Displays newer ticket IDs first.
- `fetchall()`: Retrieves all matching rows.

**Jinja2 example:**

```html
{% for ticket in tickets %}
    <tr>
        <td>{{ ticket.id }}</td>
        <td>{{ ticket.title }}</td>
        <td>{{ ticket.status }}</td>
    </tr>
{% endfor %}
```

Jinja2 allows Flask to display dynamic database content in HTML templates.

---

### 9. Git and GitHub Setup

Git tracks changes in project files.

GitHub stores the repository online.

**Important commands:**

```bash
git init
git status
git add .
git commit -m "Day 1: Initial SmartDesk Flask and SQLite setup"
git push -u origin main
```

**Git concepts:**

- Repository: A project tracked by Git.
- Commit: A saved snapshot of project changes.
- Branch: A separate line of development.
- Push: Upload local commits to a remote repository.
- `.gitignore`: Specifies files Git should ignore.

**GitHub repository:**

`SmartDesk-IT-Helpdesk`

**Initial commit:**

`Day 1: Initial SmartDesk Flask and SQLite setup`

---

### 11. Problems Encountered and Solutions

**Problem 1: PowerShell blocked virtual environment activation.**

Solution: Used a process-scoped execution policy bypass.

**Problem 2: Understanding how Flask displays database data.**

Solution: Connected SQLite to the Flask homepage and passed ticket records into `index.html` using `render_template()`.

**Problem 3: Understanding project files.**

Solution: Separated backend routes, database operations, and HTML templates into different files.

---

### 12. Day 1 Summary

During Day 1, I created the foundation of the SmartDesk IT Support Ticket Management System.

I learned how to configure a Python development environment, create a Flask application, connect to SQLite, design relational database tables, retrieve records, and display dynamic content using Jinja2.

I also initialized a Git repository and uploaded the project to GitHub.

By the end of Day 1, the application could display support tickets stored in SQLite.

### 13. Next Steps – Day 2

- Implement Create Ticket.
- Implement Read Ticket.
- Implement Update Ticket.
- Implement Delete Ticket.
- Test CRUD operations.
- Commit and push changes to GitHub.

# Day 2 Development Notes

### Ticket Management System – CRUD Operations

### 1. Day 2 Objectives

The main goal of Day 2 was to implement CRUD operations for the SmartDesk IT Support Ticket Management System using Python, Flask, SQLite, HTML, and Jinja2.

**Completed features:**
- Create new support tickets.
- View individual ticket details.
- Update existing tickets.
- Delete tickets with user confirmation.
- Validate form input.
- Handle tickets that do not exist.
- Prevent sample tickets from being recreated automatically.

---

### 2. CREATE – Create a New Ticket

**Route:** `/tickets/new`

**HTTP Methods:** GET and POST

**How it works:**
1. The user opens the Create Ticket form.
2. The user enters a title, description, and priority.
3. Flask receives the submitted data using `request.form`.
4. The application validates the input.
5. SQLite stores the new ticket using `INSERT INTO`.
6. The user is redirected to the Dashboard.

**Important SQL:**

```sql
INSERT INTO tickets
(title, description, status, priority, user_id)
VALUES (?, ?, ?, ?, ?)
```

New tickets are assigned the default status `Open`.

For now, `user_id = 1` represents the Demo User.

---

### 3. READ – View Ticket Details

**Route:** `/tickets/<int:ticket_id>`

**HTTP Method:** GET

**How it works:**
1. The user clicks View on the Dashboard.
2. Flask receives the ticket ID from the URL.
3. SQLite retrieves the matching ticket.
4. Flask renders `ticket_detail.html`.
5. If the ticket does not exist, the application returns HTTP 404.

**Important SQL:**

```sql
SELECT *
FROM tickets
WHERE id = ?
```

**Important Python method:**

`fetchone()` retrieves one database record.

**Jinja2 example:**

`{{ ticket.title }}` displays the ticket title in HTML.

---

### 4. UPDATE – Edit an Existing Ticket

**Route:** `/ticket/<int:ticket_id>/edit`

**HTTP Methods:** GET and POST

**Editable information:**
- Title
- Description
- Priority: Low, Medium, High
- Status: Open, In Progress, Resolved

**How it works:**
1. The user clicks Edit.
2. Flask loads the existing ticket information.
3. The edit form displays the current values.
4. The user modifies the information.
5. Flask validates the updated values.
6. SQLite updates the selected record.
7. The user is redirected to the ticket details page.

**Important SQL:**

```sql
UPDATE tickets
SET title = ?,
    description = ?,
    priority = ?,
    status = ?
WHERE id = ?
```

The `WHERE` clause ensures that only the selected ticket is updated.

---

### 5. DELETE – Remove a Ticket

**Route:** `/tickets/<int:ticket_id>/delete`

**HTTP Method:** POST

**How it works:**
1. The user clicks Delete.
2. JavaScript displays a confirmation message.
3. Clicking Cancel stops the deletion.
4. Clicking OK submits a POST request.
5. Flask checks whether the ticket exists.
6. SQLite deletes the selected record.
7. The user returns to the Dashboard.

**Important SQL:**

```sql
DELETE FROM tickets
WHERE id = ?
```

**Important:** Never omit the `WHERE` clause when deleting a specific ticket. Without it, all records in the table could be deleted.

---

### 6. Database Bug Fix – Sample Tickets Reappearing

**Problem:**

After deleting all tickets and restarting Flask, two sample tickets automatically appeared again.

**Cause:**

The original `database.py` contained code that checked whether the tickets table was empty:

```python
cursor.execute("SELECT COUNT(*) FROM tickets")

if cursor.fetchone()[0] == 0:
    # Insert sample tickets
```

Whenever the application restarted, `init_db()` executed this code and inserted the sample tickets again.

**Solution:**

Removed the sample ticket insertion logic from `init_db()`.

**Kept:**
- Database connection function.
- Users and tickets table creation.
- Demo User creation.
- Database commit and close operations.

**Result:**

Deleting all tickets now leaves the database empty, even after restarting Flask.

**Lesson learned:**

Database initialization should create the required database structure without automatically restoring deleted application data. Sample data should be managed separately.

---

### 7. Important Flask Concepts

| Concept | Explanation |
|---|---|
| GET | Requests a page or retrieves information |
| POST | Submits data to the server |
| `request.form` | Retrieves submitted HTML form values |
| `render_template()` | Renders an HTML template |
| `redirect()` | Redirects the browser |
| `url_for()` | Generates a URL for a Flask route |
| `fetchone()` | Retrieves one database record |
| `fetchall()` | Retrieves multiple database records |
| `commit()` | Saves database changes |
| `close()` | Closes the database connection |

---

#### 8. Testing

Manual testing checklist:

- [x] Create a ticket and verify that it appears on the Dashboard.
- [x] Open the ticket details page.
- [x] Update ticket information successfully.
- [x] Delete a ticket successfully.
- [x] Verify that deleted tickets do not reappear after restarting Flask.
- [ ] Complete the final full CRUD testing checklist before the GitHub commit.
- [ ] Confirm that invalid ticket IDs return HTTP 404.

---

### 9. Git and GitHub

After testing, the Day 2 changes should be committed and pushed to GitHub.

**Commands:**

```bash
git status
git add .
git diff --cached --stat
git commit -m "Day 2: Implement ticket CRUD operations"
git push origin main
```

**Important:** Do not commit `.venv`, `helpdesk.db`, `.env`, passwords, or other sensitive information.

---

### 10. Files Created or Updated

| File | Purpose |
|---|---|
| `app.py` | Flask routes for CRUD operations |
| `database.py` | SQLite setup and database connection |
| `templates/index.html` | Dashboard and ticket actions |
| `templates/create_ticket.html` | Create Ticket form |
| `templates/ticket_detail.html` | Ticket details page |
| `templates/edit_ticket.html` | Edit Ticket form |
| `Note.md` | Development notes |

---

### 11. Day 2 Summary

During Day 2, I implemented a complete set of CRUD operations for an IT support ticket management application.

I learned how Flask handles GET and POST requests, how to retrieve form data, and how to execute parameterized SQL statements using SQLite.

I also fixed a database initialization issue that caused deleted sample tickets to reappear after restarting the application.

These features form the foundation of the SmartDesk ticket management system.

### 12. Day 3 Goals

- User registration.
- User login and logout.
- Secure password hashing.
- User and Admin roles.
- Authentication and authorization.
- Protect ticket operations from unauthorized access.
- Add CSRF protection for state-changing requests.

# Day 3 – User Authentication & Authorization

## 1. Objectives

The goal of Day 3 was to implement user authentication and role-based authorization for the SmartDesk IT Support Ticket Management System.

By the end of Day 3, the application supports:

- User registration with password hashing.
- User login and logout.
- Session-based authentication.
- Login protection for ticket management routes.
- Ticket ownership.
- Role-based access control (User and Admin).
- Authorization checks for viewing, editing, and deleting tickets.
- HTTP 403 Forbidden responses for unauthorized access.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Flask | Web framework and routing |
| SQLite | Database for users and tickets |
| Werkzeug | Secure password hashing and verification |
| Flask Session | Maintaining login state |
| Jinja2 | Conditional HTML rendering |
| HTML | Registration, login, and ticket forms |
| Git & GitHub | Version control |

---

## 3. Database Migration

### File: `database.py`

The `users` table was updated to support authentication.

Important fields:

- `id`: Unique user identifier.
- `name`: User's full name.
- `email`: Unique email address.
- `password_hash`: Stores the hashed password.
- `role`: Determines the user's permissions.

The application uses `PRAGMA table_info(users)` to inspect the existing table and `ALTER TABLE` to add the `password_hash` column when necessary.

**Key lesson:** Database migration allows an existing database structure to be updated without deleting all existing records.

---

## 4. User Registration

### Files: `app.py`, `templates/register.html`

The registration feature allows new users to create accounts.

Registration process:

1. The user opens `/register`.
2. The user enters their name, email, password, and password confirmation.
3. Flask receives the form using a POST request.
4. The application validates the submitted data.
5. The password is hashed using Werkzeug.
6. The new user is inserted into SQLite with the default role `User`.

Example:

```python
password_hash = generate_password_hash(password)
```

The application also checks:

- Required fields are not empty.
- Password length is at least eight characters.
- Password and confirmation match.
- Email addresses are unique.

**Key lesson:** Never store plaintext passwords in the database.

---

## 5. User Login

### Files: `app.py`, `templates/login.html`

The login feature authenticates registered users.

Login process:

1. The user opens `/login`.
2. The user enters their email and password.
3. Flask retrieves the matching user from SQLite.
4. Werkzeug verifies the password against the stored hash.
5. If authentication succeeds, user information is saved in the session.
6. The user is redirected to the Dashboard.

Example:

```python
check_password_hash(user["password_hash"], password)
```

Session example:

```python
session["user_id"] = user["id"]
session["user_name"] = user["name"]
session["role"] = user["role"]
```

**Key lesson:** Authentication verifies who the user is.

---

## 6. User Logout

### File: `app.py`

The logout feature clears the user's session.

Example:

```python
session.clear()
```

The application uses a POST route for logout and redirects the user to the Login page.

**Key lesson:** Logging out removes the session information used to identify the authenticated user.

---

## 7. Login Protection

### File: `app.py`

A custom `login_required` decorator was implemented to protect application routes.

Example:

```python
@app.route("/")
@login_required
def home():
    ...
```

Protected routes include:

- Dashboard
- Create Ticket
- View Ticket
- Edit Ticket
- Delete Ticket

If the user is not authenticated, Flask redirects them to the Login page.

The decorator also verifies that the user still exists in the database.

**Key lesson:** A decorator allows authentication logic to be reused across multiple routes.

---

## 8. Ticket Ownership

### File: `app.py`

Each ticket is associated with the account that created it through the `user_id` column.

Previously, new tickets were assigned to a hardcoded user ID.

This was replaced with:

```python
user_id = session["user_id"]
```

The ticket creation SQL statement now stores the currently authenticated user's ID.

**Key lesson:** Ownership links application records to specific users and is essential for access control.

---

## 9. Dashboard Filtering

### Files: `app.py`, `templates/index.html`

The Dashboard displays different ticket lists depending on the user's role.

### Regular User

Regular users only see tickets that belong to them.

```sql
SELECT *
FROM tickets
WHERE user_id = ?
ORDER BY id DESC;
```

### Admin

Administrators can see all tickets.

```sql
SELECT *
FROM tickets
ORDER BY id DESC;
```

**Key lesson:** Database queries can filter records according to the authenticated user's permissions.

However, Dashboard filtering alone is not sufficient to secure individual ticket URLs.

---

## 10. Role-Based Authorization

### File: `app.py`

SmartDesk currently supports two roles:

| Role | Permissions |
|---|---|
| User | Manage their own tickets |
| Admin | Manage all tickets |

The application retrieves the user's role from SQLite and checks ownership before allowing access to a ticket.

Example:

```python
if ticket["user_id"] != user_id and user["role"] != "Admin":
    abort(403)
```

This authorization check is used in:

- `ticket_detail()`
- `edit_ticket()`
- `delete_ticket()`

The Edit and Delete routes check authorization before updating or deleting records.

**Key lesson:** Authorization determines what an authenticated user is allowed to do.

---

## 11. HTTP Status Codes

| Code | Meaning | Example |
|---|---|---|
| 200 | OK | Successfully viewing a page |
| 302 | Redirect | Redirecting to Login or Dashboard |
| 400 | Bad Request | Invalid form input |
| 401 | Unauthorized | Incorrect login credentials |
| 403 | Forbidden | Accessing another user's ticket |
| 404 | Not Found | Ticket does not exist |
| 409 | Conflict | Registering with an existing email |

---

## 12. Testing Performed

### Authentication

- Registered a Test User account.
- Verified password hashing.
- Logged in with registered credentials.
- Displayed the logged-in user's name.
- Logged out and cleared the session.
- Protected ticket management pages with `login_required`.

### Ticket Management

- Created tickets with the authenticated user's ID.
- Filtered Dashboard tickets by user ownership.
- Viewed and edited tickets owned by Test User.
- Tested Admin access to tickets belonging to Test User.
- Tested Admin editing and deleting another user's ticket.

### Authorization

A Flask test client was used to simulate an unauthorized deletion request.

Test case:

- Logged-in account: Test User.
- Target: Admin Private Ticket, ID #13.
- Expected result: HTTP 403 Forbidden.
- Expected database state: Ticket #13 still exists.

Actual output:

```text
HTTP Status: 403
PASS: Unauthorized deletion was blocked
PASS: Admin ticket still exists
```

**Result:** The unauthorized deletion test passed.

Direct URL checks for unauthorized View and Edit should also be confirmed and recorded as part of final testing.

---

## 13. Problems Encountered and Solutions

### Problem 1: Duplicate Flask Route

Error:

```text
AssertionError: View function mapping is overwriting an existing endpoint function: create_ticket
```

Cause: The `create_ticket()` function was defined more than once.

Solution: Removed the duplicate function and kept a single route definition.

### Problem 2: Edit Ticket Returned 404

Cause: The Edit route was temporarily unavailable or not correctly registered.

Solution: Checked the route definition and confirmed the ticket edit page opened successfully. The current route is `/ticket/<int:ticket_id>/edit`.

### Problem 3: Admin Ticket Not Found During Testing

Error:

```text
RuntimeError: Admin ticket not found
```

Cause: The test script used Ticket ID #14 instead of the actual ID #13.

Solution: Queried SQLite to identify the correct ticket ID and updated the test script.

---

## 14. Security Concepts Learned

**Authentication:** Verifies the user's identity through login credentials.

**Authorization:** Determines whether a user can access or modify a resource.

**Password Hashing:** Converts passwords into one-way hashes for safer storage.

**Session:** Stores information needed to maintain login state across requests.

**Role-Based Access Control (RBAC):** Grants permissions based on user roles.

**Ticket Ownership:** Associates a ticket with the user who created it.

**HTTP 403 Forbidden:** Indicates that an authenticated user does not have permission to access a resource.

---

## 15. Security Improvements for Future Development

Before deploying SmartDesk publicly, additional security improvements are required:

- Add CSRF protection to POST forms.
- Use a stable, securely stored Flask secret key.
- Configure secure session cookie settings for HTTPS.
- Disable Flask Debug Mode in production.
- Add login rate limiting.
- Improve error handling and user feedback.
- Expand automated tests for authentication and authorization.
- Use a production-ready WSGI server.

---

## 16. Day 3 Summary

Day 3 introduced authentication and authorization into SmartDesk.

The application now supports user registration, password hashing, login, logout, session management, protected routes, ticket ownership, and User/Admin access control.

The most important lesson was understanding the difference between **authentication (who the user is)** and **authorization (what the user is allowed to do)**.

**Day 3 Status:** Core implementation completed. Final security checks and GitHub commit remain.

# Day 4 – Ticket Search, Filtering, Sorting and Dashboard Statistics

## 1. Objectives

The main objective of Day 4 was to improve the SmartDesk dashboard by making ticket management more efficient and user-friendly.

Features implemented:
- Search tickets by title and description.
- Filter tickets by status and priority.
- Sort tickets using different sorting options.
- Display dashboard statistics.
- Maintain role-based access control.

## 2. Ticket Search

**Implementation:**

Implemented a search feature using Flask GET requests and SQLite.

The application retrieves the search keyword from the URL:

```python
search = request.args.get("search", "").strip()
search_pattern = f"%{search}%"
```

SQL uses the `LIKE` operator to search ticket titles and descriptions.

**Key concepts learned:**
- Flask query parameters (`request.args`)
- SQL `LIKE`
- Parameterized SQL queries
- Combining multiple search conditions

**Security:** Regular users can only search their own tickets, while administrators can search all tickets.

## 3. Ticket Filtering

Implemented two filtering options.

**Status Filter:**
- Open
- In Progress
- Resolved

**Priority Filter:**
- Low
- Medium
- High

Example SQL condition:

```sql
AND (? = '' OR status = ?)
AND (? = '' OR priority = ?)
```

When a filter is empty, the application displays tickets regardless of that field.

Search and filters can be used together.

**Key concepts learned:**
- Conditional SQL filtering
- Flask GET parameters
- HTML dropdown menus
- Preserving selected values using Jinja2

## 4. Ticket Sorting

Implemented five sorting options:

1. Newest First – ID descending
2. Oldest First – ID ascending
3. Priority: High to Low
4. Priority: Low to High
5. Status: A to Z

The application uses a predefined Python dictionary to control the SQL `ORDER BY` expression.

Example:

```python
sort_options = {
    "newest": "id DESC",
    "oldest": "id ASC",
    "status": "status ASC, id DESC"
}
```

Priority sorting uses SQL `CASE` expressions to define a custom order.

**Security:** Only predefined sorting expressions are accepted. User input is never inserted directly into the SQL statement.

**Key concepts learned:**
- SQL `ORDER BY`
- SQL `CASE`
- Python dictionaries
- Input validation
- Safe dynamic SQL construction

## 5. Dashboard Statistics

Implemented four dashboard statistics:

- Total Tickets
- Open Tickets
- In Progress Tickets
- Resolved Tickets

The statistics are calculated using SQLite aggregate functions.

Example:

```sql
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open,
    SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
    SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) AS resolved
FROM tickets;
```

**Role-based statistics:**
- Admin: Statistics for all tickets.
- Regular User: Statistics for tickets owned by that user.

Statistics are calculated independently of the active search and filters.

## 6. Frontend Improvements

Updated `templates/index.html` with:

- A search input.
- Status and priority dropdown menus.
- A sorting dropdown.
- Apply Filters and Clear controls.
- Four dashboard statistics cards.

Used CSS Grid to arrange the statistics cards and a media query to improve the layout on smaller screens.

**Key concepts learned:**
- HTML forms
- CSS Grid
- Responsive layouts
- Jinja2 template variables
- Integrating Flask backend data with HTML

## 7. Testing

The following functionality was tested:

- Search by ticket title and description.
- Filtering by status and priority.
- Sorting by ticket ID, priority and status.
- Combining search, filtering and sorting.
- Dashboard statistics calculations.
- Role-based ticket visibility.
- Ticket access restrictions.

**Example test result:**

For the Test User dashboard:

| Statistic | Result |
|---|---:|
| Total Tickets | 3 |
| Open Tickets | 2 |
| In Progress | 1 |
| Resolved | 0 |

These values were observed during Day 4 testing and may change as tickets are added or updated.

## 8. Problems Encountered and Solutions

**Problem 1: Python Indentation Error**

Some sorting code was placed outside the `home()` function.

Solution: Corrected indentation so that all sorting logic remained inside the function.

**Problem 2: Undefined User Variable**

Dashboard statistics code was accidentally placed inside `database.py`, causing:

`NameError: name 'user' is not defined`

Solution: Moved the statistics logic into the `home()` function in `app.py`, where the authenticated user's role is available.

**Problem 3: Role-Based Data Visibility**

Needed to ensure regular users could not access tickets belonging to other users.

Solution: Retained `WHERE user_id = ?` in user-specific queries and verified ticket access restrictions.

## 9. Day 4 Outcome

Successfully improved the SmartDesk dashboard with search, filtering, sorting and statistics features.

The application now provides a more practical ticket management interface while maintaining role-based access control.

**Next Step – Day 5:** Ticket assignment and IT Support workflow (documented below).

# Day 5 – Ticket Assignment & IT Support Workflow


## 1. Objectives and Outcome

Implemented ticket assignment and a dedicated IT Support workflow. A User creates a ticket, an Admin assigns it to IT Support, and the assigned staff member updates its status. Existing search, filtering, sorting, and dashboard statistics remain available.

## 2. Database Migration (`database.py`)

Added `tickets.assigned_to INTEGER REFERENCES users(id)` to store the assigned staff member's user ID. `NULL` means unassigned. The migration checks existing columns using `PRAGMA table_info(tickets)` before applying `ALTER TABLE`, preserving existing records.

**Key lesson:** Database schema changes can be applied incrementally without recreating the database.

## 3. Role-Based Ticket Visibility

| Role | Dashboard visibility | Assignment | Ticket status | Edit/Delete |
|---|---|---|---|---|
| Admin | All tickets | Assign/unassign | Update | Allowed |
| User | Own tickets | Not allowed | Via existing edit permissions | Own tickets |
| IT Support | Assigned tickets | Not allowed | Assigned tickets only | Not allowed |

Public registration still creates accounts with the `User` role. The `IT Support Test` account was configured for local development testing.

Updated `app.py` and `templates/index.html` to filter tickets and dashboard statistics by role. Used SQL `JOIN` for the ticket creator's name and `LEFT JOIN` for the optional assignee name. The dashboard now includes an **Assigned To** column and shows **My Assigned Tickets** for IT Support.

## 4. Ticket Assignment

**Backend:** `POST /tickets/<int:ticket_id>/assign` in `app.py`.

- Requires authentication and the Admin role.
- Checks that the ticket exists and the selected assignee has the `IT Support` role.
- Saves a valid staff ID or `NULL` for unassignment.
- Rejects unauthorized requests with HTTP `403 Forbidden`.

**Frontend:** `templates/ticket_detail.html` shows the assigned staff member and an Admin-only assignment dropdown.

## 5. IT Support Status Workflow

**Backend:** `POST /tickets/<int:ticket_id>/status` in `app.py`.

- Accepts only `Open`, `In Progress`, or `Resolved`.
- Allows Admin or the IT Support account currently assigned to the ticket.
- Saves the status in SQLite and redirects to ticket details.

**Frontend:** Assigned IT Support staff can view their tickets and use the **Update Ticket Status** form. They cannot see Admin assignment controls or use the general Edit/Delete actions.

**Key lesson:** Hiding UI buttons is not a security boundary; authorization must also be checked on the server.

## 6. Testing and Results

| Test | Result |
|---|---|
| Database migration preserves existing tickets | PASS |
| Admin assigns and unassigns a ticket | PASS |
| Regular User cannot assign tickets | PASS |
| IT Support sees assigned Ticket #14 | PASS |
| IT Support sees the status form, not the assignment form | PASS |
| Ticket #14 changes from `Open` to `In Progress` | PASS |
| SQLite and dashboard statistics reflect the new status | PASS |
| IT Support cannot assign, edit, or delete via POST | PASS (403 for each) |
| Security test preserves ticket assignment and status | PASS |

Security test output:

```text
Assignment HTTP Status: 403
Edit HTTP Status: 403
Delete HTTP Status: 403
PASS: IT Support cannot assign, edit, or delete tickets.
PASS: Ticket assignment and status remain unchanged.
```

## 7. Issues Resolved

**Missing Flask secret key:** A new PowerShell terminal did not inherit `SMARTDESK_SECRET_KEY`. Set it in that terminal before running the test:

```powershell
$env:SMARTDESK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

**Security test setup failure:** `test_assignment.py` intentionally unassigned Ticket #14 at the end, so `test_support_security.py` stopped because the ticket was not assigned. Reassigned Ticket #14 to IT Support Test (user ID 4) and reran the security test successfully.

**Key lesson:** Test scripts can change database state; test prerequisites and execution order matter.

## 8. Day 5 Summary and Next Steps

Day 5 delivered a working assignment and IT Support status workflow with tested server-side authorization. Practiced SQLite migrations, SQL joins, Flask POST routes, Jinja2 role-specific interfaces, and Flask Test Client security checks.

**Day 5 development and security testing: COMPLETED.**

**Next steps:** Save documentation and commit/push changes to GitHub. Future enhancements may include ticket comments, activity history, notifications, CSRF protection, and expanded automated tests.


---

# Day 6 – Ticket Comments and Activity History

## 1. Objectives

The goal of Day 6 was to improve communication and accountability in the SmartDesk IT Helpdesk System.

Implemented features:
- Ticket comments
- Role-based comment permissions
- Comment input validation
- Ticket activity history
- Automatic assignment activity logging
- Automatic status change logging
- Security testing

## 2. Database Improvements

### Comments Table

Created a `comments` table with the following columns:

- `id`: Unique comment identifier
- `ticket_id`: Related support ticket
- `user_id`: Comment author
- `content`: Comment text
- `created_at`: Comment creation timestamp

Added an index on `ticket_id` to improve comment retrieval.

### Ticket Activities Table

Created a `ticket_activities` table with the following columns:

- `id`: Unique activity identifier
- `ticket_id`: Related support ticket
- `user_id`: User who performed the action
- `action`: Activity type
- `details`: Description of the action
- `created_at`: Activity timestamp

Supported activity types:
- `assigned`
- `unassigned`
- `reassigned`
- `status_changed`

## 3. Ticket Comments

Implemented the following route:

`POST /tickets/<ticket_id>/comments`

Features:
- Authenticated users can submit comments.
- Users can comment on their own tickets.
- Admins can comment on any ticket.
- IT Support staff can comment on assigned tickets.
- Comments are displayed chronologically.
- Each comment displays the author's name, role, and timestamp.

## 4. Comment Security

Implemented server-side validation:

- Empty comments are rejected.
- Comments longer than 2,000 characters are rejected.
- Unauthorized comment requests return HTTP 403.
- Invalid comment requests return HTTP 400.
- Rejected comments are not saved to the database.

## 5. Ticket Activity History

Implemented automatic activity logging for:

- Assigning tickets to IT Support
- Removing ticket assignments
- Reassigning tickets
- Changing ticket status

Activities are displayed on the Ticket Details page.

Each activity includes:
- User who performed the action
- User role
- Activity description
- Timestamp

Activity records are only created when an assignment or status actually changes.

Ticket updates and activity records are saved in the same database transaction.

## 6. Testing

Successfully tested:

- IT Support commenting on assigned tickets
- IT Support being denied access to unassigned tickets
- Regular Users commenting on their own tickets
- Regular Users being denied access to other users' tickets
- Admin commenting on tickets owned by other users
- Empty comment validation
- Maximum comment length validation
- Unauthorized comments not being saved
- Automatic assignment history logging
- Automatic status change history logging
- Activity History display
- Test comment cleanup

## 7. Files Updated

- `database.py`: Added comments and ticket activity tables.
- `app.py`: Added comment handling and activity logging.
- `templates/ticket_detail.html`: Added Comments and Activity History sections.
- `test_comments.py`: Added comment functionality and security tests.

## 8. Skills Practised

- Flask routes and HTTP methods
- SQLite database relationships
- SQL JOIN queries
- Role-based access control (RBAC)
- Input validation
- Database transactions
- Automated testing with Flask Test Client
- Audit logging
- HTML and Jinja2 templates

## 9. Day 6 Outcome

SmartDesk now supports ticket-based communication and records important ticket changes.

The system provides improved collaboration between Users, Admins, and IT Support staff while maintaining role-based security.
