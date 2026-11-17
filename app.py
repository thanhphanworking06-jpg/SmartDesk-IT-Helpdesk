
# Import Flask
from flask import Flask, render_template, request, redirect, url_for

# Import database functions
from database import get_connection, init_db

# Create Flask application
app = Flask(__name__)


# Homepage - display all tickets
@app.route("/")
def home():

    # Connect to SQLite database
    connection = get_connection()

    # Get tickets and the names of their creators
    tickets = connection.execute("""
        SELECT
            tickets.id,
            tickets.title,
            tickets.description,
            tickets.status,
            tickets.priority,
            users.name AS created_by
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        ORDER BY tickets.id DESC
    """).fetchall()

    # Close database connection
    connection.close()

    # Send tickets to HTML template
    return render_template("index.html", tickets=tickets)


# Display and process the Create Ticket form
@app.route("/tickets/new", methods=["GET", "POST"])
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

        # Connect to SQLite
        connection = get_connection()

        # Save the new ticket
        connection.execute("""
            INSERT INTO tickets
            (title, description, status, priority, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            description,
            "Open",
            priority,
            1
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
def ticket_detail(ticket_id):

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
            users.name AS created_by
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        WHERE tickets.id = ?
    """, (ticket_id,)).fetchone()

    # Close database connection
    connection.close()

    # Handle ticket not found
    if ticket is None:
        return "Ticket not found", 404

    # Display ticket details
    return render_template(
        "ticket_detail.html",
        ticket=ticket
    )


# Display and process the Edit Ticket form
@app.route("/tickets/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):

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
def delete_ticket(ticket_id):

    # Connect to SQLite
    connection = get_connection()

    # Check if the ticket exists
    ticket = connection.execute(
        "SELECT id FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    # Handle ticket not found
    if ticket is None:
        connection.close()
        return "Ticket not found", 404

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

# Start Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
