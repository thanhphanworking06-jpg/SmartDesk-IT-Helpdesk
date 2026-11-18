
# Test ticket deletion authorization
from app import app
from database import get_connection

# Change this to the actual Admin ticket ID
ADMIN_TICKET_ID = 13

# Connect to the database
connection = get_connection()

# Find the regular Test User
user = connection.execute("""
    SELECT id
    FROM users
    WHERE email = ?
""", ("testuser@example.com",)).fetchone()

# Find the Admin ticket
ticket = connection.execute("""
    SELECT id, user_id
    FROM tickets
    WHERE id = ?
""", (ADMIN_TICKET_ID,)).fetchone()

connection.close()

# Validate test setup before sending a DELETE request
if user is None:
    raise RuntimeError("Test User not found")

if ticket is None:
    raise RuntimeError("Admin ticket not found")

if ticket["user_id"] == user["id"]:
    raise RuntimeError("This ticket belongs to Test User")

# Create a Flask test client
client = app.test_client()

# Simulate a logged-in Test User
with client.session_transaction() as test_session:
    test_session["user_id"] = user["id"]
    test_session["user_name"] = "Test User"
    test_session["role"] = "User"

# Attempt to delete another user's ticket
response = client.post(
    f"/tickets/{ADMIN_TICKET_ID}/delete",
    follow_redirects=False
)

# Check the response
print("HTTP Status:", response.status_code)

# Verify the ticket still exists
connection = get_connection()

remaining_ticket = connection.execute(
    "SELECT id FROM tickets WHERE id = ?",
    (ADMIN_TICKET_ID,)
).fetchone()

connection.close()

assert response.status_code == 403, "Expected 403 Forbidden"
assert remaining_ticket is not None, "Ticket was unexpectedly deleted"

print("PASS: Unauthorized deletion was blocked")
print("PASS: Admin ticket still exists")
