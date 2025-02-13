from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/674f5423f73deab1e9a7"
blog_data = requests.get(blog_url).json()

@app.route("/")
def home():
  return render_template("index.html", blog_post=blog_data)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id):
  post_item = None
  for blog_post in blog_data:
    if blog_post["id"] == post_id:
      post_item = blog_post
  print(post_item)
  return render_template("post.html", post_item=post_item)

if __name__ == "__main__":
    app.run(debug=True)


