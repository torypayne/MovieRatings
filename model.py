from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session



ENGINE = create_engine("sqlite:///ratings.db", echo=False)
s = scoped_session(sessionmaker(bind=ENGINE, 
                                    autocommit = False, 
                                    autoflush = False))

Base = declarative_base()
Base.query = s.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    released_at = Column(Integer, nullable=True)
    imdb_url = Column(String(150), nullable=True)

class Rating(Base):
    __tablename__= "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=user_id))
    movie = relationship("Movie", backref=backref("ratings", order_by=movie_id))

### End class declarations
def create_user(email, password, password_verify):
    check_email = s.query(User).filter_by(email = email).first()
    print check_email
    if check_email != None:
        return 1
    elif hash(password) != hash(password_verify):
        return 2
    else:
        add_user = User(email=email, password=password)
        s.add(add_user)
        s.commit()
        return 3


def authenticate(email, password):
    check_email = s.query(User).filter_by(email = email).first()
    print check_email
    if check_email == None:
        return None
    password_input = hash(password)
    real_password = s.query(User.password).filter_by(email=email).first()
    real_password = hash(real_password[0])
    if password_input == real_password:
        print "That password checked out"
        return email
    else:
        print "Not a good password nub"
        return None



# def connect():
#     global ENGINE
#     global s

#     return s()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
