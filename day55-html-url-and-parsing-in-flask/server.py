from flask import Flask
import random

random_number = random.randint(0, 9)

app = Flask(__name__)

# def check_guess_wrapper(func):
# def wrapper(*args):
#   if args[0] == random_number:
#     return "<h1>You found me !</h1>" \
#             "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>" 
#   elif args[0] > random_number:
#     return "<h1>Too high, try again !</h1>" \
#             "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>" 
#   else:
#     return "<h1>Too low, try again !</h1>" \
#             "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>" 


    
@app.route("/")
def home():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>"

@app.route("/<int:guess_number>")
def wrapper(guess_number):
  if guess_number == random_number:
    return "<h1>You found me !</h1>" \
            "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>" 
  elif guess_number > random_number:
    return "<h1>Too high, try again !</h1>" \
            "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>" 
  else:
    return "<h1>Too low, try again !</h1>" \
            "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>" 


 

app.run(debug=True)