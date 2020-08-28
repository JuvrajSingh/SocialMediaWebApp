import sqlite3
from flask import render_template

ROOT = path.dirname(path.relpath((__file__)))

def checkLogin(username, password):
    """Confirms whether Login details are correct"""

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
    """Checks whether username is taken, and if not then stores the new users details in database"""

    # Query database for username
    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", username)
    users = cur.fetchall()

    # Ensure username not already taken
    if len(users) != 0:
        return False
    
    else:
        # pwHash = generate password hash TODO
        cur.execute("INSERT INTO users (username, hash), VALUES (?, ?)", username, pwHash)

        # Save changes in file
        con.commit()
        # Close connection
        con.close()

        return True


def apology(message):
    return render_template("apology.html", message=message)