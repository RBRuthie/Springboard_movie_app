from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


#  define the class
#  the class user will inherit from the model sqlalchemy database

# user mixin provides flask-log in information about the user with the class model. Does not affect the database
class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# favorite table database - store user favorite movie
class Favorite(db.Model):
    __tablename__ = "favorites"
    
    username = db.Column(db.String(25), db.ForeignKey("users.username"), primary_key=True,)
    movie = db.Column(db.String(25), primary_key=True, nullable=False)

