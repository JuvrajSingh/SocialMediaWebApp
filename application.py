from flask import Flask, render_template, request, session, redirect

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

        # TODO

        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")