from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User


# customer validator (invlid credentials function) for login page, checking user name and password
def invalid_credentials(form, field):
    
    username_entered = form.username.data
    password_entered  = field.data
    
    user_object = User.query.filter_by(username=username_entered).first()
    
    # checking if login credentials are valid
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
   
    # check if password entered matches password stored in database
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")




# ******************** DEFINE REGISTRATION FORM & validators *******************************

class RegistrationForm(FlaskForm):
    """ Registration form """
    

# StringField('username' = name of the field is username
    username = StringField('username',
         validators=[InputRequired(message="Username required"),
         Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    
    password = PasswordField('password',
         validators=[InputRequired(message="Password required"),
         Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    
    confirm_pswd = PasswordField('confirm_pswd',
         validators=[InputRequired(message="Password required"),
         EqualTo('password', message="Passwords must match")])
    
    submit_button = SubmitField('Register')
    
# this is an inline custom validator
# error catching 
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        # incase the username is duplicate
        if user_object:
             raise ValidationError("Username already exist, select different username")
    
    
# ******************** LOGIN FORM *******************************

class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('username', validators=[InputRequired(message="Username required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])   
    submit_button = SubmitField('Login')
    
    

        
        

    
    