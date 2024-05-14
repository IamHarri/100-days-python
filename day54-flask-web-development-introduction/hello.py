from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
 
if __name__ == "__main__": # it means current running file name is __main__ #ex ramdom.__name__ (=> __main__)
    app.run()