from flask import Flask, render_template, request, session, redirect
from models import checkLogin

app = Flask(__name__)

@app.route("/")
@login_required
def index():
    # TODO

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            # return apology("Must provide username")
        elif not request.form.get("password"):
            # return apology("Must provide password")

        loginSuccess, user_id = checkLogin(request.form.get("username"), request.form.get("password"))
        
        if  loginSuccess = False:
            # return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user_id

        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")