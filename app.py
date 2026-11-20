
# Import Flask
from flask import Flask, render_template, request, redirect, url_for, session, abort

# Import password security functions
from werkzeug.security import generate_password_hash, check_password_hash

# Import other libraries
import sqlite3
import os
from functools import wraps

# Import database functions
from database import get_connection, init_db

# Create Flask application
app = Flask(__name__)

# Configure secret key for user sessions
app.config["SECRET_KEY"] = os.environ.get("SMARTDESK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SMARTDESK_SECRET_KEY is not configured")

# Require users to log in before accessing protected pages
def login_required(view_function):

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        # Check whether a user is logged in
        if "user_id" not in session:
            return redirect(url_for("login"))

        # Check whether the user still exists in the database
        connection = get_connection()

        user = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        connection.close()

        # Clear invalid sessions
        if user is None:
            session.clear()
            return redirect(url_for("login"))

        # Continue to the requested page
        return view_function(*args, **kwargs)

    return wrapper



# Display the ticket dashboard
@app.route("/")
@login_required
def home():

    # Get the logged-in user's ID
    user_id = session["user_id"]

    # Get the search keyword from the URL
    search = request.args.get("search", "").strip()

    # Get the selected filters from the URL
    status_filter = request.args.get("status", "").strip()
    priority_filter = request.args.get("priority", "").strip()

    # Get the selected sorting option
    sort_by = request.args.get("sort", "newest").strip()

    # Safe sorting expressions use explicit ticket table aliases
    sort_options = {
        "newest": "t.id DESC",
        "oldest": "t.id ASC",
        "priority_high": "CASE t.priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END, t.id DESC",
        "priority_low": "CASE t.priority WHEN 'Low' THEN 1 WHEN 'Medium' THEN 2 WHEN 'High' THEN 3 ELSE 4 END, t.id DESC",
        "status": "t.status ASC, t.id DESC"
    }
    if sort_by not in sort_options:
        sort_by = "newest"
    if status_filter not in ("", "Open", "In Progress", "Resolved"):
        status_filter = ""
    if priority_filter not in ("", "Low", "Medium", "High"):
        priority_filter = ""

    connection = get_connection()
    try:
        user = connection.execute(
            "SELECT role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if user is None:
            session.clear()
            return redirect(url_for("login"))

        current_role = user["role"]
        if current_role == "Admin":
            visibility_sql = "1 = 1"
            visibility_params = []
        elif current_role == "IT Support":
            visibility_sql = "t.assigned_to = ?"
            visibility_params = [user_id]
        else:
            visibility_sql = "t.user_id = ?"
            visibility_params = [user_id]

        tickets = connection.execute(f"""
            SELECT t.*, creator.name AS created_by,
                   support.name AS assigned_to_name
            FROM tickets AS t
            JOIN users AS creator ON creator.id = t.user_id
            LEFT JOIN users AS support ON support.id = t.assigned_to
            WHERE {visibility_sql}
              AND (t.title LIKE ? OR t.description LIKE ?)
              AND (? = '' OR t.status = ?)
              AND (? = '' OR t.priority = ?)
            ORDER BY {sort_options[sort_by]}
        """, (*visibility_params, f"%{search}%", f"%{search}%",
              status_filter, status_filter, priority_filter, priority_filter)).fetchall()

        stats = connection.execute(f"""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN t.status = 'Open' THEN 1 ELSE 0 END) AS open,
                   SUM(CASE WHEN t.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
                   SUM(CASE WHEN t.status = 'Resolved' THEN 1 ELSE 0 END) AS resolved
            FROM tickets AS t
            WHERE {visibility_sql}
        """, visibility_params).fetchone()
    finally:
        connection.close()

    return render_template(
        "index.html", tickets=tickets, search=search,
        status_filter=status_filter, priority_filter=priority_filter,
        sort_by=sort_by, stats=stats, current_role=current_role
    )

# Display and process the Create Ticket form
@app.route("/tickets/new", methods=["GET", "POST"])
@login_required
def create_ticket():

    # Check if the user submitted the form
    if request.method == "POST":

        # Get data from the HTML form
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")

        # Validate the form data
        if not title or not description:
            return "Title and description are required.", 400

        if priority not in ["Low", "Medium", "High"]:
            return "Invalid priority.", 400

        # Get the currently logged-in user's ID
        user_id = session["user_id"]

        # Connect to SQLite
        connection = get_connection()

        # Save the new ticket with its actual owner
        connection.execute("""
            INSERT INTO tickets
            (title, description, status, priority, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            description,
            "Open",
            priority,
            user_id
        ))

        # Save changes and close connection
        connection.commit()
        connection.close()

        # Return to the dashboard
        return redirect(url_for("home"))

    # Show the form when using GET
    return render_template("create_ticket.html")

# Display details of a single ticket
@app.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    user_id = session["user_id"]
    connection = get_connection()
    try:
        ticket = connection.execute("""
            SELECT t.*, creator.name AS created_by,
                   support.name AS assigned_to_name
            FROM tickets AS t
            JOIN users AS creator ON creator.id = t.user_id
            LEFT JOIN users AS support ON support.id = t.assigned_to
            WHERE t.id = ?
        """, (ticket_id,)).fetchone()
        if ticket is None:
            abort(404)
        user = connection.execute(
            "SELECT role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if user is None:
            session.clear()
            return redirect(url_for("login"))
        current_role = user["role"]
        is_assigned_support = (
            current_role == "IT Support" and ticket["assigned_to"] == user_id
        )
        if (ticket["user_id"] != user_id
                and current_role != "Admin"
                and not is_assigned_support):
            abort(403)
        support_users = []
        if current_role == "Admin":
            support_users = connection.execute("""
                SELECT id, name FROM users
                WHERE role = 'IT Support' ORDER BY name ASC
            """).fetchall()
    finally:
        connection.close()
    return render_template(
        "ticket_detail.html", ticket=ticket,
        current_role=current_role, support_users=support_users,
        can_update_status=(current_role == "Admin" or is_assigned_support)
    )


# Update ticket status: only Admin or assigned IT Support
@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
@login_required
def update_ticket_status(ticket_id):
    new_status = request.form.get("status", "").strip()
    if new_status not in ("Open", "In Progress", "Resolved"):
        abort(400)
    connection = get_connection()
    try:
        user = connection.execute(
            "SELECT role FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        ticket = connection.execute(
            "SELECT assigned_to FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            abort(404)
        if user is None or not (
            user["role"] == "Admin" or
            (user["role"] == "IT Support" and ticket["assigned_to"] == session["user_id"])
        ):
            abort(403)
        connection.execute(
            "UPDATE tickets SET status = ? WHERE id = ?", (new_status, ticket_id)
        )
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


@app.route("/tickets/<int:ticket_id>/assign", methods=["POST"])
@login_required
def assign_ticket(ticket_id):
    user_id = session["user_id"]
    connection = get_connection()

    try:
        # Read the current role from the database, not the session
        current_user = connection.execute("""
            SELECT role FROM users WHERE id = ?
        """, (user_id,)).fetchone()

        if current_user is None or current_user["role"] != "Admin":
            abort(403)

        # Make sure the requested ticket exists
        ticket = connection.execute("""
            SELECT id FROM tickets WHERE id = ?
        """, (ticket_id,)).fetchone()
        if ticket is None:
            abort(404)

        # Empty selection means remove the current assignment
        selected_user = request.form.get("assigned_to", "").strip()
        if selected_user == "":
            support_id = None
        else:
            try:
                support_id = int(selected_user)
            except ValueError:
                abort(400, description="Invalid support user ID.")

            if support_id <= 0:
                abort(400, description="Invalid support user ID.")

            # Assign tickets only to users with the IT Support role
            support_user = connection.execute("""
                SELECT id FROM users
                WHERE id = ? AND role = 'IT Support'
            """, (support_id,)).fetchone()
            if support_user is None:
                abort(400, description="Selected user is not IT Support.")

        connection.execute("""
            UPDATE tickets SET assigned_to = ? WHERE id = ?
        """, (support_id, ticket_id))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


# Display and process the Edit Ticket form
@app.route("/ticket/<int:ticket_id>/edit", methods=["GET", "POST"])
@login_required
def edit_ticket(ticket_id):

    # Get the currently logged-in user's ID
    user_id = session["user_id"]

    # Connect to SQLite
    connection = get_connection()

    # Find the ticket
    ticket = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    # Handle ticket not found
    if ticket is None:
        connection.close()
        return "Ticket not found", 404

    # Get the logged-in user's role
    user = connection.execute("""
        SELECT role
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    # Handle invalid user session
    if user is None:
        connection.close()
        session.clear()
        return redirect(url_for("login"))

    # Check ticket ownership and admin permission
    if ticket["user_id"] != user_id and user["role"] != "Admin":
        connection.close()
        abort(403)

    # Process the submitted form
    if request.method == "POST":

        # Get updated information
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "")
        status = request.form.get("status", "")

        # Validate form data
        if not title or not description:
            connection.close()
            return "Title and description are required.", 400

        if priority not in ["Low", "Medium", "High"]:
            connection.close()
            return "Invalid priority.", 400

        if status not in ["Open", "In Progress", "Resolved"]:
            connection.close()
            return "Invalid status.", 400

        # Update the ticket in SQLite
        connection.execute("""
            UPDATE tickets
            SET title = ?,
                description = ?,
                priority = ?,
                status = ?
            WHERE id = ?
        """, (
            title,
            description,
            priority,
            status,
            ticket_id
        ))

        # Save changes
        connection.commit()
        connection.close()

        # Redirect to the updated ticket details
        return redirect(
            url_for("ticket_detail", ticket_id=ticket_id)
        )

    # Show the form with existing ticket data
    connection.close()

    return render_template(
        "edit_ticket.html",
        ticket=ticket
    )

# Delete a ticket
@app.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
@login_required
def delete_ticket(ticket_id):

    # Get the currently logged-in user's ID
    user_id = session["user_id"]

    # Connect to SQLite
    connection = get_connection()

    # Check if the ticket exists and get its owner
    ticket = connection.execute(
        "SELECT id, user_id FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    # Handle ticket not found
    if ticket is None:
        connection.close()
        return "Ticket not found", 404

    # Get the logged-in user's role
    user = connection.execute("""
        SELECT role
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    # Handle invalid user session
    if user is None:
        connection.close()
        session.clear()
        return redirect(url_for("login"))

    # Check ticket ownership and admin permission
    if ticket["user_id"] != user_id and user["role"] != "Admin":
        connection.close()
        abort(403)

    # Delete the selected ticket
    connection.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    # Save changes
    connection.commit()
    connection.close()

    # Return to the dashboard
    return redirect(url_for("home"))

# Register a new user
@app.route("/register", methods=["GET", "POST"])
def register():

    # Process the registration form
    if request.method == "POST":

        # Get information from the form
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check required fields
        if not name or not email or not password:
            return "All fields are required.", 400

        # Check password length
        if len(password) < 8:
            return "Password must be at least 8 characters.", 400

        # Check matching passwords
        if password != confirm_password:
            return "Passwords do not match.", 400

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        # Connect to SQLite
        connection = get_connection()

        try:
            # Insert a new user with the default User role
            connection.execute("""
                INSERT INTO users
                (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                password_hash,
                "User"
            ))

            # Save the new account
            connection.commit()

        except sqlite3.IntegrityError:
            # Handle duplicate email addresses
            return "This email is already registered.", 409

        finally:
            # Always close the database connection
            connection.close()

        # Show success message
        return "Registration successful! Login will be added next."

    # Display the registration form
    return render_template("register.html")

# Login an existing user
@app.route("/login", methods=["GET", "POST"])
def login():

    # Check if the login form was submitted
    if request.method == "POST":

        # Get email and password from the form
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validate required fields
        if not email or not password:
            return "Email and password are required.", 400

        # Connect to SQLite
        connection = get_connection()

        # Find the user by email
        user = connection.execute("""
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        connection.close()

        # Check the email and password
        if (
            user is None
            or not user["password_hash"]
            or not check_password_hash(
                user["password_hash"], password
            )
        ):
            return "Invalid email or password.", 401

        # Clear previous session information
        session.clear()

        # Save logged-in user information
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["role"] = user["role"]

        # Redirect to Dashboard
        return redirect(url_for("home"))

    # Display the Login form
    return render_template("login.html")

# Log out the current user
@app.route("/logout", methods=["POST"])
def logout():

    # Remove all user information from the session
    session.clear()

    # Redirect to the Login page
    return redirect(url_for("login"))

# Start Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
