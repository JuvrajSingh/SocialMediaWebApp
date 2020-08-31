import sqlite3 as sql
from flask import render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
from functools import wraps

ROOT = path.dirname(path.relpath((__file__)))

def checkLogin(username, password):
    """Confirms whether Login details are correct"""

    # Query database for username
    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    con.row_factory = sql.Row  # Makes tuple hashable I think (hopefully)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    users = cur.fetchall()

    # Ensure username exists and password is correct
    if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
        return False, username
    else:
        return True, users[0]["id"]


def registerUser(username, password):
    """Checks whether username is taken, and if not then stores the new users details in database"""

    # Query database for username
    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    users = cur.fetchall()

    # Ensure username not already taken
    if len(users) != 0:
        return False
    
    else:
        pwHash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, pwHash))

        con.commit()  # Save changes in file
        con.close()  # Close connection

        return True


def apology(message):
    return render_template("apology.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def createPost(content):
    """Stores the post submitted by the current user in the database"""

    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    user_id = session["user_id"]
    cur.execute("INSERT INTO posts (name, content) VALUES ((SELECT username FROM users WHERE id = ?), ?)", (user_id, content))
    con.commit()  # Save changes in file
    con.close()  # Close connection


def getPosts():
    """Returns all posts from people that current user is following"""

    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    user_id = session["user_id"]
    cur.execute("SELECT username FROM users WHERE id = ?", [user_id])
    name = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM posts WHERE name IN (SELECT following FROM followers WHERE user = ?) OR name = ?", (name, name))
    posts = cur.fetchall()
    return posts


def getPersons():
    """Returns a list of the names of all users in the database excluding the current user"""

    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    user_id = session["user_id"]
    cur.execute("SELECT username FROM users WHERE NOT username = (SELECT username FROM users WHERE id = ?)", [user_id])
    tempPersons = cur.fetchall()
    persons = []
    for person in tempPersons:
        persons.append(person[0])
    return persons


def followUser(following):
    """Updates database to show who current user is now following"""

    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    cur = con.cursor()
    user_id = session["user_id"]
    cur.execute("INSERT INTO followers (user, following) VALUES ((SELECT username FROM users WHERE id = ?), ?)", (user_id, following))
    con.commit()  # Save changes in file
    con.close()  # Close connection