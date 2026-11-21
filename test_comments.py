
from app import app
from database import get_connection

TICKET_ID = 14
SUPPORT_EMAIL = "support@test.com"
TEST_COMMENT = "Day 6 test: Investigating this ticket."

app.config["TESTING"] = True

# Find the IT Support account
connection = get_connection()

support = connection.execute("""
    SELECT id, role
    FROM users
    WHERE email = ?
""", (SUPPORT_EMAIL,)).fetchone()

ticket = connection.execute("""
    SELECT id, assigned_to
    FROM tickets
    WHERE id = ?
""", (TICKET_ID,)).fetchone()

connection.close()

if support is None or support["role"] != "IT Support":
    raise RuntimeError("IT Support account not found.")

if ticket is None:
    raise RuntimeError("Ticket #14 not found.")

if ticket["assigned_to"] != support["id"]:
    raise RuntimeError("Ticket #14 is not assigned to IT Support Test.")

# Simulate an authenticated IT Support session
client = app.test_client()

with client.session_transaction() as sess:
    sess["user_id"] = support["id"]
    sess["role"] = support["role"]

# Submit a test comment
response = client.post(
    f"/tickets/{TICKET_ID}/comments",
    data={"content": TEST_COMMENT},
    follow_redirects=False
)

print("Comment POST HTTP Status:", response.status_code)

assert response.status_code == 302

# Verify that the comment was saved
connection = get_connection()

saved_comment = connection.execute("""
    SELECT id, ticket_id, user_id, content
    FROM comments
    WHERE ticket_id = ? AND user_id = ? AND content = ?
    ORDER BY id DESC
    LIMIT 1
""", (TICKET_ID, support["id"], TEST_COMMENT)).fetchone()

connection.close()

assert saved_comment is not None

print("Saved Comment:", dict(saved_comment))
print("PASS: IT Support comment saved successfully.")

# Security Test: IT Support cannot comment on an unassigned ticket
UNASSIGNED_TICKET_ID = 13

# Count comments before the unauthorized request
connection = get_connection()

before_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (UNASSIGNED_TICKET_ID,)).fetchone()["total"]

connection.close()

# Attempt to comment on a ticket not assigned to IT Support
response = client.post(
    f"/tickets/{UNASSIGNED_TICKET_ID}/comments",
    data={"content": "Unauthorized IT Support comment"},
    follow_redirects=False
)

print("Unauthorized Comment HTTP Status:", response.status_code)

# The backend must reject this request
assert response.status_code == 403

# Verify that the rejected comment was not saved
connection = get_connection()

after_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (UNASSIGNED_TICKET_ID,)).fetchone()["total"]

connection.close()

assert before_count == after_count

print("PASS: IT Support cannot comment on unassigned tickets.")
print("PASS: Unauthorized comment was not saved.")

# Security Test: Reject invalid comment content

# Count comments before testing invalid inputs
connection = get_connection()
before_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (TICKET_ID,)).fetchone()["total"]
connection.close()

# Test 1: Empty comment
response = client.post(
    f"/tickets/{TICKET_ID}/comments",
    data={"content": "   "},
    follow_redirects=False
)

print("Empty Comment HTTP Status:", response.status_code)
assert response.status_code == 400

# Test 2: Comment exceeding 2000 characters
response = client.post(
    f"/tickets/{TICKET_ID}/comments",
    data={"content": "A" * 2001},
    follow_redirects=False
)

print("Long Comment HTTP Status:", response.status_code)
assert response.status_code == 400

# Verify that invalid comments were not saved
connection = get_connection()
after_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (TICKET_ID,)).fetchone()["total"]
connection.close()

assert before_count == after_count

print("PASS: Empty comments are rejected.")
print("PASS: Comments over 2000 characters are rejected.")
print("PASS: Invalid comments were not saved.")



# Security Test: Regular User permissions

USER_ID = 2
OWN_TICKET_ID = 8
OTHER_TICKET_ID = 13

connection = get_connection()

user = connection.execute("""
    SELECT id, role
    FROM users
    WHERE id = ?
""", (USER_ID,)).fetchone()

own_ticket = connection.execute("""
    SELECT id, user_id
    FROM tickets
    WHERE id = ?
""", (OWN_TICKET_ID,)).fetchone()

other_ticket = connection.execute("""
    SELECT id, user_id
    FROM tickets
    WHERE id = ?
""", (OTHER_TICKET_ID,)).fetchone()

connection.close()

# Verify test data before running
assert user is not None and user["role"] == "User"
assert own_ticket is not None and own_ticket["user_id"] == USER_ID
assert other_ticket is not None and other_ticket["user_id"] != USER_ID

# Simulate a regular User session
user_client = app.test_client()

with user_client.session_transaction() as sess:
    sess["user_id"] = USER_ID
    sess["role"] = "User"

# Test 1: User can comment on their own ticket
response = user_client.post(
    f"/tickets/{OWN_TICKET_ID}/comments",
    data={"content": "User permission test comment"},
    follow_redirects=False
)

print("User Own Ticket HTTP Status:", response.status_code)
assert response.status_code == 302

# Test 2: User cannot comment on another user's ticket
connection = get_connection()

before_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (OTHER_TICKET_ID,)).fetchone()["total"]

connection.close()

response = user_client.post(
    f"/tickets/{OTHER_TICKET_ID}/comments",
    data={"content": "Unauthorized regular user comment"},
    follow_redirects=False
)

print("User Other Ticket HTTP Status:", response.status_code)
assert response.status_code == 403

# Verify unauthorized comment was not saved
connection = get_connection()

after_count = connection.execute("""
    SELECT COUNT(*) AS total
    FROM comments
    WHERE ticket_id = ?
""", (OTHER_TICKET_ID,)).fetchone()["total"]

connection.close()

assert before_count == after_count

print("PASS: User can comment on their own ticket.")
print("PASS: User cannot comment on another user's ticket.")
print("PASS: Unauthorized User comment was not saved.")


# Security Test: Admin can comment on tickets owned by other users

ADMIN_ID = 3
ADMIN_TEST_TICKETS = [8, 14]

connection = get_connection()

admin = connection.execute("""
    SELECT id, role
    FROM users
    WHERE id = ?
""", (ADMIN_ID,)).fetchone()

tickets = connection.execute("""
    SELECT id, user_id
    FROM tickets
    WHERE id IN (?, ?)
""", tuple(ADMIN_TEST_TICKETS)).fetchall()

connection.close()

# Verify test data
assert admin is not None and admin["role"] == "Admin"
assert len(tickets) == len(ADMIN_TEST_TICKETS)
assert all(ticket["user_id"] != ADMIN_ID for ticket in tickets)

# Simulate an authenticated Admin session
admin_client = app.test_client()

with admin_client.session_transaction() as sess:
    sess["user_id"] = ADMIN_ID
    sess["role"] = "Admin"

# Admin should be allowed to comment on both tickets
for ticket_id in ADMIN_TEST_TICKETS:
    comment_text = f"Admin permission test for ticket {ticket_id}"

    response = admin_client.post(
        f"/tickets/{ticket_id}/comments",
        data={"content": comment_text},
        follow_redirects=False
    )

    print(f"Admin Ticket #{ticket_id} HTTP Status:", response.status_code)
    assert response.status_code == 302

    # Verify that the comment was saved
    connection = get_connection()

    saved_comment = connection.execute("""
        SELECT id
        FROM comments
        WHERE ticket_id = ?
          AND user_id = ?
          AND content = ?
        ORDER BY id DESC
        LIMIT 1
    """, (ticket_id, ADMIN_ID, comment_text)).fetchone()

    connection.close()

    assert saved_comment is not None

print("PASS: Admin can comment on tickets owned by other users.")
print("PASS: Admin comments were saved successfully.")


# Day 6: Clean up comments created by this test run
# Remove only test comments, not real user comments

TEST_COMMENTS = [
    (14, 4, "Day 6 test: Investigating this ticket."),
    (8, 2, "User permission test comment"),
    (8, 3, "Admin permission test for ticket 8"),
    (14, 3, "Admin permission test for ticket 14"),
]

connection = get_connection()

try:
    for ticket_id, user_id, content in TEST_COMMENTS:
        connection.execute("""
            DELETE FROM comments
            WHERE ticket_id = ?
              AND user_id = ?
              AND content = ?
              AND id NOT IN (1, 2, 13)
        """, (ticket_id, user_id, content))

    connection.commit()
    print("PASS: Test comments cleaned up.")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()


