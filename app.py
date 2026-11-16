
# Import Flask
from flask import Flask, render_template

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


# Start Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
