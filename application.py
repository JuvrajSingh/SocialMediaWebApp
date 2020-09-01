from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_cors import CORS
from tempfile import mkdtemp

from models import checkLogin, registerUser, apology, login_required, createPost, getPosts, getMyPosts, getPersons, getFollowers, followUser, unfollowUser, deletePost


app = Flask(__name__)

CORS(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        post = request.form.get("post")
        # Check to make sure user hasn't left field blank
        if not post:
            return apology("Please enter something to post")
        # Create post and store it in database
        createPost(post)

    # Get posts from the database from people current user is following
    posts = getPosts()
    posts.reverse()

    return render_template("index.html", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            return apology("Must provide username")
        elif not password:
            return apology("Must provide password")

        loginSuccess, user_id = checkLogin(username, password)
        
        if loginSuccess == False:
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user_id

        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted and not already taken
        if not username:
            return apology("Must provide username")
        # Ensure both password fields submitted
        if not password or not confirmation:
            return apology("Please enter a password and confirm it")
        # Ensure both password fields match
        if password != confirmation:
            return apology("Passwords must match")

        if registerUser(username, password) == False:
            return apology("Sorry, that username is already taken")

        # Redirect user to index/login page
        return redirect("/")
    
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/people")
@login_required
def people():
    """Displays a list of all users and allows current user to follow them"""

    persons = getPersons()
    followers = getFollowers()
    return render_template("people.html", persons=persons, followers=followers)

@app.route("/follow/<following>")
@login_required
def follow(following):
    """Current user follows user they requested to follow"""
    
    followUser(following)
    return redirect("/")

@app.route("/unfollow/<following>")
@login_required
def unfollow(following):
    """Current user unfollows user they requested"""

    unfollowUser(following)
    return redirect("/")

@app.route("/myPosts")
def myPosts():
    # Get all of current users' posts from database
    posts = getMyPosts()
    posts.reverse()

    return render_template("myPosts.html", posts=posts)

@app.route("/delete/<post_id>")
def delete(post_id):
    """Remove post from database"""

    deletePost(post_id)
    return redirect("/")