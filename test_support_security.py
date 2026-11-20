
from app import app
from database import get_connection

# Security test configuration
TICKET_ID = 14
SUPPORT_EMAIL = "support@test.com"

app.config["TESTING"] = True

# Find the IT Support account
connection = get_connection()

support = connection.execute("""
    SELECT id, name, role
    FROM users
    WHERE email = ?
""", (SUPPORT_EMAIL,)).fetchone()

if support is None or support["role"] != "IT Support":
    connection.close()
    raise RuntimeError("IT Support account not found.")

# Read the current ticket assignment
ticket = connection.execute("""
    SELECT id, assigned_to, status
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

if ticket is None:
    raise RuntimeError("Test ticket not found.")

if ticket["assigned_to"] != support["id"]:
    raise RuntimeError(
        "Ticket #14 must be assigned to IT Support Test."
    )

original_assignment = ticket["assigned_to"]
original_status = ticket["status"]

# Create an authenticated IT Support client
client = app.test_client()

with client.session_transaction() as sess:
    sess["user_id"] = support["id"]
    sess["user_name"] = support["name"]
    sess["role"] = support["role"]

# Test A: IT Support cannot assign tickets
response = client.post(
    f"/tickets/{TICKET_ID}/assign",
    data={"assigned_to": ""},
    follow_redirects=False
)

print("Assignment HTTP Status:", response.status_code)

assert response.status_code == 403

# Test B: IT Support cannot edit ticket details
response = client.post(
    f"/ticket/{TICKET_ID}/edit",
    data={
        "title": "Unauthorized Change",
        "description": "Security test",
        "priority": "High",
        "status": "Resolved"
    },
    follow_redirects=False
)

print("Edit HTTP Status:", response.status_code)

assert response.status_code == 403

# Test C: IT Support cannot delete tickets
response = client.post(
    f"/tickets/{TICKET_ID}/delete",
    follow_redirects=False
)

print("Delete HTTP Status:", response.status_code)

assert response.status_code == 403

# Verify that the ticket remains unchanged
connection = get_connection()

updated_ticket = connection.execute("""
    SELECT id, assigned_to, status
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

assert updated_ticket is not None
assert updated_ticket["assigned_to"] == original_assignment
assert updated_ticket["status"] == original_status

print("PASS: IT Support cannot assign, edit, or delete tickets.")
print("PASS: Ticket assignment and status remain unchanged.")
