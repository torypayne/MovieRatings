from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session



ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, 
                                    autocommit = False, 
                                    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

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
# def connect():
#     global ENGINE
#     global Session

#     return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
