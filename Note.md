# SmartDesk – IT Support Ticket Management System

## Day 1 – Project Setup & Database

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
└── Note.txt
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

### 10. Git and GitHub Setup

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

## SmartDesk – Day 2 Development Notes
## Ticket Management System – CRUD Operations

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

**Route:** `/tickets/<int:ticket_id>/edit`

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

Kept:
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

### 8. SQL Commands Learned

**INSERT:** Add new records.

**SELECT:** Retrieve existing records.

**UPDATE:** Modify existing records.

**DELETE:** Remove records.

**SQL placeholders (`?`):** Pass values separately from SQL statements to help prevent SQL injection.

---

### 9. Testing

Manual testing checklist:

- [x] Create a ticket and verify that it appears on the Dashboard.
- [x] Open the ticket details page.
- [x] Update ticket information successfully.
- [x] Delete a ticket successfully.
- [x] Verify that deleted tickets do not reappear after restarting Flask.
- [ ] Complete the final full CRUD testing checklist before the GitHub commit.
- [ ] Confirm that invalid ticket IDs return HTTP 404.

---

### 10. Git and GitHub

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

### 11. Files Created or Updated

| File | Purpose |
|---|---|
| `app.py` | Flask routes for CRUD operations |
| `database.py` | SQLite setup and database connection |
| `templates/index.html` | Dashboard and ticket actions |
| `templates/create_ticket.html` | Create Ticket form |
| `templates/ticket_detail.html` | Ticket details page |
| `templates/edit_ticket.html` | Edit Ticket form |
| `Note.txt` | Development notes |

---

### 12. Day 2 Summary

During Day 2, I implemented a complete set of CRUD operations for an IT support ticket management application.

I learned how Flask handles GET and POST requests, how to retrieve form data, and how to execute parameterized SQL statements using SQLite.

I also fixed a database initialization issue that caused deleted sample tickets to reappear after restarting the application.

These features form the foundation of the SmartDesk ticket management system.

### 13. Day 3 Goals

- User registration.
- User login and logout.
- Secure password hashing.
- User and Admin roles.
- Authentication and authorization.
- Protect ticket operations from unauthorized access.
- Add CSRF protection for state-changing requests.