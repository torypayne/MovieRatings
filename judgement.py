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
        user_email = session.get("email")
        user = model.s.query(model.User).filter_by(email = user_email).first()
        user = user.id
        return redirect(url_for("user_page", user_id=user))
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
    user_email = session.get("email")
    user = model.s.query(model.User).filter_by(email = user_email).first()
    user = user.id
    home = (url_for("user_page", user_id=user))
    user_list = model.s.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list, home=home)

@app.route("/movies")
def movies():
    user_email = session.get("email")
    user = model.s.query(model.User).filter_by(email = user_email).first()
    user = user.id
    home = (url_for("user_page", user_id=user))
    movie_list = model.s.query(model.Movie).limit(50).all()
    return render_template("movie_list.html", movies=movie_list, home=home)

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
    user_email = session.get("email")
    home_user = model.s.query(model.User).filter_by(email = user_email).first()
    home_user = home_user.id
    home = (url_for("user_page", user_id=home_user))
    user = model.s.query(model.User).filter_by(id=user_id).first()
    return render_template("user.html", user=user, home=home)

@app.route("/movie/<movie_id>")
def movie_page(movie_id):
    user_email = session.get("email")
    home_user = model.s.query(model.User).filter_by(email = user_email).first()
    home_user = home_user.id
    home = (url_for("user_page", user_id=home_user))
    user = model.s.query(model.User).filter_by(email = user_email).first()
    movie = model.s.query(model.Movie).filter_by(id=movie_id).first()
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == user.id:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    #prediction code - should only run if a movie hasn't been rated yet
    
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
    else:
        effective_rating = user_rating.rating

    the_eye = model.s.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
    eye_rating = model.s.query(model.Rating).filter_by(user_id=the_eye.id,
            movie_id=movie.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot.",
             "I am a golden god and all should fear me.  And your taste is terrible.",
             "Your judgment is the peak of insanity.",
             "I hate you.",
             "I enjoy watching how wrong you are.",
             "You're fired.",
             "I'd rather be watching Toddlers & Tiaras than listen to your BS.",
             "I love hedgehogs."]


    beratement = messages[int(2*difference)]

    return render_template("movie.html", movie=movie, home=home,
                            average=avg_rating, user_rating=user_rating,
                            prediction=prediction, beratement=beratement)



@app.route("/movie/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    user_email = session.get("email")
    user = model.s.query(model.User).filter_by(email = user_email).first()
    user = user.id
    rating_value = request.form.get("rating")
    rating_check = model.s.query(model.Rating).filter_by(movie_id=movie_id, user_id=user).first()
    if rating_check != None:
        rating_check.rating = rating_value
        model.s.commit()
        flash("Your rating has been updated!")
        return redirect(url_for("movie_page", movie_id=movie_id))
    else:
        add_rating = model.Rating(movie_id=movie_id, user_id =user, rating = rating_value)
        model.s.add(add_rating)
        model.s.commit()
        flash("You rating has been submitted!")
        return redirect(url_for("movie_page", movie_id=movie_id))

if __name__ == "__main__":
    app.run(debug = True)