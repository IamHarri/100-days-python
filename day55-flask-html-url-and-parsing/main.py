from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
 
 
@app.route("/username/<name>/<int:number>")
def greet(name, number):
  return f'<h1 style="text-align: center; color: green">hello there {name}, you are {number} years old</h1>' \
    '<p>This is my paragraph</p>' \
    '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2Exam9kZWRrNGUxNWRpa3YybDdtbmV6bzNwOXZxem1tcDZsc28wcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/btjkkkawtefIY/giphy.gif" width="500">'

if __name__ == "__main__": # it means current running file name is __main__ #ex ramdom.__name__ (=> __main__)
    app.run(debug=True)