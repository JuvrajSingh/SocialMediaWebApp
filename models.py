import sqlite3

ROOT = path.dirname(path.relpath((__file__)))

def checkLogin(username, password):
    # Query database for username
    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", username)
    users = cur.fetchall()

    # Ensure username exists and password is correct
    if len(users) != 1: # or not check_password_hash(. .) TODO
        return False, username
    else:
        return True, users[0]["id"]


def registerUser(username, password):
    # TODO