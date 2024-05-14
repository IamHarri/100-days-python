from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route('/')
def home():
  return render_template("home.html")

@app.route("/guess/<name>")
def guess(name):
  gender_url=f"https://api.genderize.io/?name={name}"
  gender_data = requests.get(gender_url)
  gender = gender_data.json()["gender"]
  age_url = f"https://api.agify.io/?name={name}"
  age_data = requests.get(age_url).json()
  age = age_data["age"]
  return render_template("index.html",name=name, gender=gender, age=age)

@app.route("/blog/<num>")
def blog(num):
  print(num)
  blog_url = "https://api.npoint.io/676476690114489c4345"
  blog_data = requests.get(blog_url).json()
  return render_template("blog.html", blog_post=blog_data)
if __name__ == "__main__": 
  app.run(debug=True)
