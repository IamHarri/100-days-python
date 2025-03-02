from flask import Flask, jsonify, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
# import pandas
import random
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

# with app.app_context():
#   new_cafe = Cafe(
#     name="Cafe Example",
#     map_url="https://example.com/map",
#     img_url="https://example.com/image.jpg",
#     location="New York, NY",
#     seats="50",
#     has_toilet=True,
#     has_wifi=True,
#     has_sockets=True,
#     can_take_calls=True,
#     coffee_price="5.00"
#   )

# db.session.add(new_cafe)
# db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record

@app.route("/random", methods=('GET','POST'))
def get_random_coffee():
  with app.app_context():
    result = db.session.execute(db.select(Cafe))
    all_cafe = result.scalars().all()
    cafe = random.choice(all_cafe)
    cafe.to_dict()
    return jsonify(cafe=cafe.to_dict())

@app.route("/all", methods=('GET',))
def get_all_coffee():
  with app.app_context():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    all_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes)

@app.route("/search", methods=('GET',))
def search_coffee():
  query_location = request.args.get('loc')
  with app.app_context():
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


# HTTP POST - Create Record
@app.route("/add", methods=('GET','POST'))
def create_coffee():
  with app.app_context():
    new_cafe = Cafe(
      name=request.form.get('name'),
      map_url=request.form.get('map_url'),
      img_url=request.form.get('img_url'),
      location=request.form.get('location'),
      seats=request.form.get('seats'),
      has_toilet=bool(request.form.get('has_toilet')),
      has_wifi=bool(request.form.get('has_wifi')),
      has_sockets=bool(request.form.get('has_sockets')),
      can_take_calls=bool(request.form.get('can_take_calls')),
      coffee_price=request.form.get('coffee_price')
    )
  db.session.add(new_cafe)
  db.session.commit()
  return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    # cafe = db.get_or_404(Cafe, cafe_id) # NOTE: this solution can not handle the not found case.
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

    
# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
  api_key = request.args.get("api-key")
  if api_key != "TopSecretAPIKey":
    return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api-key."}), 403
  # cafe = db.get_or_404(Cafe, cafe_id)
  cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
  if cafe:
    db.session.delete(cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully deleted the cafe."})
  else:
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})
  
if __name__ == '__main__':
    app.run(debug=True) 


