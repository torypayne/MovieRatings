from flask import Flask, render_template, redirect, request, url_for, flash, session
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("email"):
        return redirect(url_for("users"))
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    if model.authenticate(email, password):
        flash("You're in!")
        session['email'] = email
    else:
        flash("No movie ratings for you!")
    return redirect(url_for("index"))

@app.route("/logout")
def clear_session():
    session.clear()
    flash("You logged out.")
    print "You logged out!!"
    return redirect(url_for("index"))

@app.route("/users")
def users():
    user_list = model.s.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    password_verify = request.form.get("password_verify")
    response = model.create_user(email, password, password_verify)
    if response == 1:
        flash("That email is already in use. Please log in or use another.")
        return redirect(url_for("register"))
    elif response == 2:
        flash("Passwords do not match. Please try again.")
        return redirect(url_for("register"))
    else:
        flash("Success! Please log in to rate movies.")
        return redirect(url_for("index"))

@app.route("/user/<user_id>")
def user_page(user_id):
    user = model.s.query(model.User).filter_by(id=user_id).first()
    return render_template("user.html", user=user)

@app.route("/movie/<movie_id>")
def movie_page(movie_id):
    movie = model.s.query(model.Movie).filter_by(id=movie_id).first()
    return render_template("movie.html", movie=movie)

if __name__ == "__main__":
    app.run(debug = True)