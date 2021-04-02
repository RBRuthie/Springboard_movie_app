
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user
from dotenv import load_dotenv, find_dotenv

import os
import json
import urllib.request


# importing from other files
from form_fields import *
from models import *


#  configure app
app = Flask(__name__)
load_dotenv(find_dotenv())


#************************     DATABASE      ************************************************

# configure the data base
# its an app secret key to encription cookies, anythig pertaining to the app
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")
# location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
# os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db_user = os.environ.get('DB_USER')
print(db_user)

connect_db(app)

#************************   END OF  DATABASE  ************************************************



# Initialize login manager  -  user login/logout
login = LoginManager(app)
login.init_app(app)


#  load users for when login/out - loads the user and returns a user object
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# user logout
@app.route("/logout", methods=['GET'])
def logout():

    # Logout user
    logout_user()
    # flash('You have logged out successfully')
    return redirect(url_for('index'))



#  **************************    ROUTES      *************


#  home - landing page
@app.route('/')
def index():
    api_key = os.environ.get("API_KEY")
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={}&page=1'.format(api_key)
    data = urllib.request.urlopen(url).read()
    data = json.loads(data)
    return render_template('index.html', movies=data["results"])


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data["query"]
    api_key = os.environ.get("API_KEY")
    url = 'https://api.themoviedb.org/3/search/movie?&api_key={}&page=1&query={}'.format(api_key, query)
    data = urllib.request.urlopen(url).read()
    return data


#  *** signup/registration route ***
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  
    # instantiate the registration form
    reg_form = RegistrationForm()
    
    # update the database if validation is sucessful
    if reg_form.validate_on_submit():
          username = reg_form.username.data
          password = reg_form.password.data
          
          # hash password
          hashed_pswd = pbkdf2_sha256.hash(password)
    
          # add user to database
          user = User(username=username, password=hashed_pswd)
          db.session.add(user)
          db.session.commit()
          # when a user successfully register we will redirect the user to log in page 
        #   flash('Registered succesfully. Please login.')
          return redirect(url_for('login'))
         
    return render_template('signup.html', form=reg_form)
  
  


#  *** login route ***
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # instantiate the login form
    login_form = LoginForm()
    
    # update the database if validation is sucessful
    if login_form.validate_on_submit():
    
        # getting username from database and matching to the username submitted in the log in form
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        resp = redirect(url_for('mypage'))
        resp.set_cookie('user',login_form.username.data)
        return resp
        
    return render_template("login.html", form=login_form)
  
  
  
#   user account page - protection
@app.route("/mypage", methods=['GET', 'POST'])
def mypage():

    if not current_user.is_authenticated:
        # flash('Please login', 'danger')
        # return redirect(url_for('login'))
        flash('Please login.')
    user = request.cookies.get('user')
    favorites = [f.movie for f in Favorite.query.filter_by(username=user).all()]
    api_key = os.environ.get("API_KEY")
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={}&page=1'.format(api_key)
    data = urllib.request.urlopen(url).read()
    movies = json.loads(data)["results"]
    return render_template("mypage.html", user=user, movies=movies, favorites=json.dumps(favorites))
    # return "my page"
    
    
    
#  popular movies tab 
@app.route('/popular_movies', methods=['GET', 'POST'])
def popular_movies():
    api_key = os.environ.get("API_KEY")
    url = 'https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page=1'.format(api_key)
    data = urllib.request.urlopen(url).read()
    data = json.loads(data)
    return render_template('popular_movies.html', movies=data["results"])


#  tv-show tab
@app.route('/tv_shows', methods=['GET', 'POST'])
def tv_shows():
    api_key = os.environ.get("API_KEY")
    url ='https://api.themoviedb.org/3/tv/popular?api_key={}&language=en-US&page=1'.format(api_key)
    data = urllib.request.urlopen(url).read()
    data = json.loads(data)
    return render_template('tv_shows.html', movies=data["results"])


#  whatt's trending tab
@app.route('/whats_trending', methods=['GET', 'POST'])
def whats_trending():
    api_key = os.environ.get("API_KEY")
    url ='https://api.themoviedb.org/3/trending/all/day?api_key={}'.format(api_key)
    data = urllib.request.urlopen(url).read()
    data = json.loads(data)
    return render_template('whats_trending.html', movies=data["results"])


#  favorite tab
@app.route('/favorite', methods=['GET', 'POST', 'DELETE'])
def favorite():
    if request.method == 'GET':
        user = request.cookies.get('user')
        favorites = [f.movie for f in Favorite.query.filter_by(username=user).all()] 
        api_key = os.environ.get("API_KEY")
        url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'
        movies = [json.loads(urllib.request.urlopen(url.format(id, api_key)).read())for id in favorites]
        return render_template('favorite.html', movies=json.dumps(movies))
    elif request.method == 'POST':
        data = request.json
        user, movie = data["user"], data["movie"]
        favorite = Favorite(username=user, movie=movie)
        db.session.add(favorite)
        db.session.commit()
        return "movie added to favorite"
    else:
        data = request.json
        user, movie = data["user"], data["movie"]
        Favorite.query.filter(Favorite.username==user).filter(Favorite.movie==movie).delete()
        db.session.commit()
        return "movie removed from favorite"






  
if __name__ == '__main__':
    app.run(debug=True)