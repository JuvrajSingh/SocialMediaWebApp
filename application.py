from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_cors import CORS
from tempfile import mkdtemp

from models import checkLogin, registerUser, apology, login_required, createPost, getPosts, getMyPosts


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
        # Create post and store it in database
        createPost(session["user_id"], post)

    # Get all the posts from the database
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

@app.route("/myPosts", methods=["GET", "POST"])
def myPosts():
    if request.method == "POST":
        post_id = request.form.get("post_id")
        # Remove post from database
        deletePost(post_id)

    # Get all of current users' posts from database
    posts = getMyPosts(session["user_id"])
    posts.reverse()

    return render_template("myPosts.html", posts=posts)