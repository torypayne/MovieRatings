import model
import csv

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
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(model.Session)
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
