
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


# Create database tables and apply migrations
def init_db():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Table 1: Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT,
                role TEXT NOT NULL DEFAULT 'User'
            )
        """)

        # Check existing columns in the users table
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [
            column["name"] for column in cursor.fetchall()
        ]

        # Add password_hash column if missing
        if "password_hash" not in user_columns:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN password_hash TEXT
            """)

        # Add role column if missing
        if "role" not in user_columns:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN role TEXT NOT NULL DEFAULT 'User'
            """)

        # Supported user roles:
        # User       - Creates and tracks own tickets
        # Admin      - Manages all tickets and assignments
        # IT Support - Works on assigned tickets

        # Table 2: Tickets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                priority TEXT NOT NULL DEFAULT 'Medium',
                user_id INTEGER NOT NULL,
                assigned_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (assigned_to) REFERENCES users(id)
            )
        """)

        # Check existing columns in the tickets table
        cursor.execute("PRAGMA table_info(tickets)")
        ticket_columns = [
            column["name"] for column in cursor.fetchall()
        ]

        # Add assigned_to column for existing databases
        if "assigned_to" not in ticket_columns:
            cursor.execute("""
                ALTER TABLE tickets
                ADD COLUMN assigned_to INTEGER
                REFERENCES users(id)
            """)

            print(
                "Migration completed: "
                "assigned_to column added."
            )

        # Table 3: Comments
        # Store messages related to support tickets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id)
                    REFERENCES tickets(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
            )
        """)

        # Index for faster comment retrieval by ticket
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_comments_ticket_id
            ON comments(ticket_id)
        """)

        print("Comments table initialized successfully!")


        # Table 4: Ticket Activity History
        # Store important ticket actions and changes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id)
                    REFERENCES tickets(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
            )
        """)

        # Index for faster activity history retrieval
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_activities_ticket_id
            ON ticket_activities(ticket_id)
        """)

        print("Ticket activity history table initialized successfully!")

        # Add a demo user for testing
        # INSERT OR IGNORE prevents duplicate demo users
        cursor.execute("""
            INSERT OR IGNORE INTO users (
                id, name, email, role
            )
            VALUES (
                1, 'Demo User', 'demo@example.com', 'User'
            )
        """)

        # Sample tickets are not created automatically.
        # New tickets must be created through the website.

        # Save all database changes
        connection.commit()

        print("Database initialized successfully!")

    except sqlite3.Error:
        # Roll back changes if a database error occurs
        connection.rollback()
        raise

    finally:
        # Always close the database connection
        connection.close()


# Run database setup
if __name__ == "__main__":
    init_db()
