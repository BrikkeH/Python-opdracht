from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__, template_folder='template')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(days=1)

@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        flash("Hi, "+ user + "! You logged in!")
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

@app.route("/over")
def test():
    if "user" in session:
        return render_template("over.html")
    else:
        return redirect(url_for("login"))

@app.route("/home")
def gohome():
    return redirect(url_for("home"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("home"))
        #return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")

#@app.route("/user")
#def user():
#    if "user" in session:
#        user = session["user"]
#        return "<h1>Hi, "+ user + "</h1>"
#    else:
#        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!")
    session.pop("user", None)
    return redirect(url_for("login"))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)