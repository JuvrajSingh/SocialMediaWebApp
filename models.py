import sqlite3 as sql
from flask import render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
from functools import wraps

ROOT = path.dirname(path.relpath((__file__)))


def initialise(option, connection=False):
    """
    Initialises for use of sqlite3
    If connection is True will also return con
    options:
    1 - return only cur;
    2 - return only cur, but as a hashable tuple
    3 - return cur and user_id
    Return order - cur, user_id, con
    """

    con = sql.connect(path.join(ROOT, "socialMedia.db"))
    if option == 2:
        con.row_factory = sql.Row
        cur = con.cursor()
        if connection == False:
            return cur
        else:
            return cur, con
    else:
        cur = con.cursor()
        if option == 1:
            if connection == False:
                return cur
            else:
                return cur, con
        # Otherwise must be option 3
        user_id = session["user_id"]
        if connection == False:
            return cur, user_id
        else:
            return cur, user_id, con


def finish(con):
    """Commits and closes sql connection after saving changes"""

    con.commit()  # Save changes in file
    con.close()  # Close connection


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


def checkLogin(username, password):
    """Confirms whether Login details are correct"""

    # Query database for username
    cur = initialise(2)
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
    cur, con = initialise(1, True)
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    users = cur.fetchall()

    # Ensure username not already taken
    if len(users) != 0:
        return False
    
    else:
        pwHash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, pwHash))

        finish(con)

        return True


def createPost(content):
    """Stores the post submitted by the current user in the database"""

    cur, user_id, con = initialise(3, True)
    cur.execute("INSERT INTO posts (name, content) VALUES ((SELECT username FROM users WHERE id = ?), ?)", (user_id, content))
    finish(con)


def getPosts():
    """Returns all posts from people that current user is following"""

    cur, user_id = initialise(3)
    cur.execute("SELECT username FROM users WHERE id = ?", [user_id])
    name = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM posts WHERE name IN (SELECT following FROM followers WHERE user = ?) OR name = ?", (name, name))
    posts = cur.fetchall()
    return posts


def getMyPosts():
    cur, user_id = initialise(3)
    cur.execute("SELECT username FROM users WHERE id = ?", [user_id])
    name = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM posts WHERE name = ?", [name])
    posts = cur.fetchall()
    return posts


def getPersons():
    """Returns a list of the names of all users in the database excluding the current user"""

    cur, user_id = initialise(3)
    cur.execute("SELECT username FROM users WHERE NOT username = (SELECT username FROM users WHERE id = ?)", [user_id])
    tempPersons = cur.fetchall()
    persons = []
    for person in tempPersons:
        persons.append(person[0])
    return persons


def getFollowers():
    """Returns a list of names of poeple that the current user is following"""

    cur, user_id = initialise(3)
    cur.execute("SELECT following FROM followers WHERE user = (SELECT username FROM users WHERE id = ?)", [user_id])
    tempFollowers = cur.fetchall()
    followers = []
    for follower in tempFollowers:
        followers.append(follower[0])
    return followers


def followUser(following):
    """Updates database to show who current user is now following"""

    cur, user_id, con = initialise(3, True)
    cur.execute("INSERT INTO followers (user, following) VALUES ((SELECT username FROM users WHERE id = ?), ?)", (user_id, following))
    finish(con)


def unfollowUser(following):
    """Updates database to show current user is no longer following selected user"""
    
    cur, user_id, con = initialise(3, True)
    cur.execute("DELETE FROM followers WHERE user = (SELECT username FROM users WHERE id = ?) AND following = ?", (user_id, following))
    finish(con)


#def deletePost(post):
