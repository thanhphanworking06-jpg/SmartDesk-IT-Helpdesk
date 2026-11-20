
from app import app
from database import get_connection

# Test ticket assignment
TICKET_ID = 14
SUPPORT_ID = 4

# Find an existing Admin account
connection = get_connection()

admin = connection.execute("""
    SELECT id, name
    FROM users
    WHERE role = 'Admin'
    LIMIT 1
""").fetchone()

connection.close()

if admin is None:
    raise RuntimeError("No Admin account found.")

# Create Flask test client
app.config["TESTING"] = True
client = app.test_client()

# Simulate an authenticated Admin session
with client.session_transaction() as sess:
    sess["user_id"] = admin["id"]
    sess["user_name"] = admin["name"]
    sess["role"] = "Admin"

# Assign ticket to IT Support
response = client.post(
    f"/tickets/{TICKET_ID}/assign",
    data={"assigned_to": str(SUPPORT_ID)},
    follow_redirects=False
)

print("HTTP Status:", response.status_code)

# Verify assignment in database
connection = get_connection()

ticket = connection.execute("""
    SELECT id, title, assigned_to
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

print("Ticket ID:", ticket["id"])
print("Ticket Title:", ticket["title"])
print("Assigned To:", ticket["assigned_to"])

assert response.status_code == 302
assert ticket["assigned_to"] == SUPPORT_ID

print("PASS: Admin successfully assigned the ticket.")


# Test 6: Regular User cannot assign tickets

connection = get_connection()

regular_user = connection.execute("""
    SELECT id, name
    FROM users
    WHERE role = 'User'
      AND password_hash IS NOT NULL
    LIMIT 1
""").fetchone()

connection.close()

if regular_user is None:
    raise RuntimeError("No regular test user found.")

# Create a separate client for the regular user
user_client = app.test_client()

with user_client.session_transaction() as sess:
    sess["user_id"] = regular_user["id"]
    sess["user_name"] = regular_user["name"]
    sess["role"] = "User"

# Attempt to remove the assignment
response = user_client.post(
    f"/tickets/{TICKET_ID}/assign",
    data={"assigned_to": ""},
    follow_redirects=False
)

print("User HTTP Status:", response.status_code)

# Check that the assignment remains unchanged
connection = get_connection()

ticket = connection.execute("""
    SELECT assigned_to
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

print("Assigned To After User Attempt:", ticket["assigned_to"])

assert response.status_code == 403
assert ticket["assigned_to"] == SUPPORT_ID

print("PASS: Regular User cannot assign tickets.")


# Test 7: Admin can unassign a ticket

# Use the authenticated Admin test client
response = client.post(
    f"/tickets/{TICKET_ID}/assign",
    data={"assigned_to": ""},
    follow_redirects=False
)

print("Unassign HTTP Status:", response.status_code)

# Verify the assignment was removed
connection = get_connection()

ticket = connection.execute("""
    SELECT id, assigned_to
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

print("Assigned To After Unassign:", ticket["assigned_to"])

assert response.status_code == 302
assert ticket["assigned_to"] is None

print("PASS: Admin successfully unassigned the ticket.")
