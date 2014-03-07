import model
import csv
import datetime

#open a file
#read a line
#parse a line
#create an object
#add object to session
#commit
#repeat

def load_users(session):
    with open("./seed_data/u.user", "rb") as f:
        reader = csv.reader(f, delimiter="|")
        session = model.Session()
        for row in reader:
            add_user = model.User(age=row[1], zipcode=row[4])
            session.add(add_user)
        session.commit()

def load_movies(session):
    with open("./seed_data/u.item", "rb") as f:
        reader = csv.reader(f, delimiter="|")
        session = model.Session()
        for row in reader:
            title =  row[1]
            title = title.split(" (")
            title = title[0]
            title = title.decode("latin-1")
            if row[2] == '':
                dt = datetime.datetime.strptime("01-Jan-1970", "%d-%b-%Y")
            else:
                dt = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            # print dt
            # print "IMDB url="+row[4]
            add_movie = model.Movie(name=title, released_at=dt, imdb_url=row[4])
            session.add(add_movie)
        session.commit()
    

def load_ratings(session):
    # use u.data
    with open("./seed_data/u.data", "rb") as f:
        reader = csv.reader(f, delimiter="\t")
        session = model.Session()
        for row in reader:
            # dt = datetime.datetime.utcfromtimestamp(float(row[3]))
            add_rating = model.Rating(movie_id=row[1], user_id=row[0], rating=row[2])
            session.add(add_rating)
        session.commit()
            
    

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(model.Session)
    load_movies(model.Session)
    load_ratings(model.Session)
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
