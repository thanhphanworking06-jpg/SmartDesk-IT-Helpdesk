
import sqlite3

# Database filename
DB_NAME = "helpdesk.db"


# Connect to SQLite database
def get_connection():
    # Open the database or create it if it does not exist
    connection = sqlite3.connect(DB_NAME)

    # Allow accessing columns by name
    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# Create database tables
def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    # Table 1: Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL
        )
    """)

    # Table 2: Tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            priority TEXT NOT NULL DEFAULT 'Medium',
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Add a demo user for testing
    # INSERT OR IGNORE prevents duplicate demo users
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, name, email, role)
        VALUES (1, 'Demo User', 'demo@example.com', 'User')
    """)

    # Sample tickets are no longer created automatically.
    # New tickets must be created through the website.

    # Save changes to the database
    connection.commit()

    # Close the database connection
    connection.close()


# Run database setup
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
