
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

    # Connect to SQLite
    connection = get_connection()

    # Read the user's current role from the database
    user = connection.execute("""
        SELECT role
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    if user is None:
        connection.close()
        session.clear()
        return redirect(url_for("login"))

    # Admin can see all tickets
    if user["role"] == "Admin":

        tickets = connection.execute("""
            SELECT *
            FROM tickets
            ORDER BY id DESC
        """).fetchall()

    # Regular users can only see their own tickets
    else:

        tickets = connection.execute("""
            SELECT *
            FROM tickets
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,)).fetchall()

    # Close database connection
    connection.close()

    # Display the dashboard
    return render_template("index.html", tickets=tickets)

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

    # Get the currently logged-in user's ID
    user_id = session["user_id"]

    # Connect to SQLite
    connection = get_connection()

    # Find the ticket by ID
    ticket = connection.execute("""
        SELECT
            tickets.id,
            tickets.title,
            tickets.description,
            tickets.status,
            tickets.priority,
            tickets.created_at,
            tickets.user_id,
            users.name AS created_by
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        WHERE tickets.id = ?
    """, (ticket_id,)).fetchone()

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

    # Close database connection
    connection.close()

    # Handle invalid user session
    if user is None:
        session.clear()
        return redirect(url_for("login"))

    # Check ticket ownership and admin permission
    if ticket["user_id"] != user_id and user["role"] != "Admin":
        abort(403)

    # Display ticket details
    return render_template(
        "ticket_detail.html",
        ticket=ticket
    )

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
