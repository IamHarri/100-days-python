from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250))
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250))

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
      return f'<Movie {self.title}>'

with app.app_context():
    db.create_all()

# CREATE FORM
class MovieForm(FlaskForm):
    rating = StringField(label='Your rating out of 10, eg. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField(label='Done', )


# ADD MOVIE FORM
class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie', )
# with app.app_context():
#   new_movie = Movie(
#       # title="Phone Booth",
#       # year=2002,
#       # description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#       # rating=7.3,
#       # ranking=10,
#       # review="My favourite character was the caller.",
#       # img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"

#       title="Avatar The Way of Water",
#       year=2022,
#       description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#       rating=7.3,
#       ranking=9,
#       review="I liked the water.",
#       img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#   )
#   db.session.add(new_movie)
#   db.session.commit()

@app.route("/")
def home():
  with app.app_context():
    result = db.session.execute(db.select(Movie).order_by(Movie.id))
    all_movies = result.scalars().all()
    for movie in all_movies:
      print(movie.img_url)  # Accessing img_url from each Movie object
  return render_template("index.html",movies=all_movies  )

@app.route('/edit/<int:id>', methods=('GET','POST'))
def edit(id):
  form = MovieForm()
  # with app.app_context():
  #   result = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
  if request.method == "POST":
    movie_id = id
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        # or movie_to_update = db.get_or_404(Movie, movie_id)  
        movie_to_update.rating = request.form['rating']
        movie_to_update.review = request.form['review']
        db.session.commit()  
    return redirect(url_for('home'))
  return render_template('edit.html', form=form)


@app.route('/delete/<int:id>', methods=('GET','POST'))
def delete(id):
  movie_id = id
  with app.app_context():
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    # or movie_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
  return redirect(url_for('home'))

@app.route('/add', methods=('GET','POST'))
def add():
  form = AddMovieForm()
  return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
