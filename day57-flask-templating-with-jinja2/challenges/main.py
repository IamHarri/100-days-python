from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_data = requests.get("https://api.npoint.io/676476690114489c4345").json()
@app.route('/')
def home():
    return render_template("index.html",blog_data=blog_data)
@app.route('/post/<post_id>')
def post(post_id):
    print(post_id)
    return render_template("post.html",blog_data=blog_data,post_id=post_id)

if __name__ == "__main__":
    app.run(debug=True)
