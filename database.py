
import sqlite3

# Database filename
DB_NAME = "helpdesk.db"


# Connect to SQLite database
def get_connection():
    connection = sqlite3.connect(DB_NAME) #Lệnh này mở kết nối tới helpdesk.db. Nếu file chưa tồn tại, SQLite sẽ tự tạo file.
    connection.row_factory = sqlite3.Row
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


    # Add a demo user
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, name, email, role)
        VALUES (1, 'Demo User', 'demo@example.com', 'User')
    """)

    # Check if sample tickets already exist
    cursor.execute("SELECT COUNT(*) FROM tickets")

    if cursor.fetchone()[0] == 0:
        # Ticket 1
        cursor.execute("""
            INSERT INTO tickets
            (title, description, status, priority, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Laptop cannot connect to Wi-Fi",
            "Unable to connect to office Wi-Fi",
            "Open",
            "High",
            1
        ))

        # Ticket 2
        cursor.execute("""
            INSERT INTO tickets
            (title, description, status, priority, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Outlook not receiving emails",
            "New emails are not appearing",
            "In Progress",
            "Medium",
            1
        ))

    connection.commit() #lưu các thay đổi vào database.
    connection.close() #đóng kết nối sau khi hoàn thành.


# Run database setup
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
