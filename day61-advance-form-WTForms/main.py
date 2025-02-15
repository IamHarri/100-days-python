from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from flask_bootstrap import Bootstrap5

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
match_email="admin@email.com"
match_password="12345678"

def check_password_len(form, field):
    if len(field.data) < 8:
        raise ValidationError('Field must be at least 8 characters long')
def check_email(form,field):
    if "@" not in field.data:
        raise ValidationError('Invalid email address')
    
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), check_email])
    password = PasswordField(label='Password', validators=[DataRequired(), check_password_len])
    submit = SubmitField(label="Log In")

app = Flask(__name__)
app.secret_key = "oajfioasdjoifj"
bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=('GET', 'POST'))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
      email=login_form.email.data
      password=login_form.password.data
      if email == match_email and password == match_password:
        return render_template('success.html')
      return render_template('denied.html')
    return render_template('login.html', form=login_form)

# @app.route("/sucess")
# def sucess():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
