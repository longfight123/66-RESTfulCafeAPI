"""My RESTful Cafe's API

This 'Flask' app creates a Cafe's API website that the user can make HTTP requests to
query for a random cafe, query for all cafes, search for a specific cafe on location,
add a new cafe, update the price of a cafe or delete a cafe. Data is stored inside an SQLite database.
The landing page has a link to the documentation for the API.

This script requires that 'Flask' and 'Flask-SQLAlchemy' be installed within the Python
environment you are running this script in.
"""

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nhbuoufzzsoqhj:3d4f4f55a4780ca446a400545e4bdad12efaaf8b4b5b0466671110870c1d5d7c@ec2-3-218-149-60.compute-1.amazonaws.com:5432/d8k7fnu25o8v3k'#os.environ.get('DATABASE_URL', 'sqlite:///cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

try:
    db.create_all()
except:
    pass



##Cafe TABLE Configuration
class Cafe(db.Model):
    """
    A class used to represent a Cafe record in a database.
    ...
    Attributes
    ----------
    id: db.Column
        an integer column representing the primary key
    name: db.Column
        a string column representing the name of the cafe
    map_url: db.Column
        a string column representing the URL to the location of the cafe
    img_url: db.Column
        a string column representing a URL to an image of the cafe
    seats: db.Column
        a string column representing a range of the quantity of seats in the cafe
    has_toilet: db.Column
        a boolean column to represent the presence of toilets
    has_wifi: db.Column
        a boolean column to represent the presence of wifi
    has_sockets: db.Column
        a boolean column to represent the presence of power sockets
    can_take_calls: db.Column
        a boolean column to represent the ability to call the cafe
    coffee_price: db.Column
        a string column to represent the relative price of coffee at the cafe

    Methods
    -------
    to_dict()
        converts a record in the database to a dictionary
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """converts a cafe record in the database into a dictionary

        Returns
        -------
        dict
            a dictionary of the column names and the values for a record in the cafe database
        """
        dict = {}
        for column in self.__table__.columns:
            dict[column.name] = getattr(self, column.name)
        return dict

try:
    newcafe = Cafe(id=1, name='Science Gallary London',
                   map_url='https://g.page/scigallerylon?share',
                   img_url='https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg',
                   location='London Bridge',
                   has_sockets=1,
                   has_toilet=1,
                   has_wifi=1,
                   can_take_calls=1,
                   seats='50+',
                   coffee_price='100'
                   )
    newcafe1 = Cafe(id=2, name='Social - Copeland Road',
                   map_url='https://g.page/CopelandSocial?share',
                   img_url='https://images.squarespace-cdn.com/content/v1/5734f3ff4d088e2c5b08fe13/1555848382269-9F13FE1WQDNUUDQOAOXF/ke17ZwdGBToddI8pDm48kAeyi0pcxjZfLZiASAF9yCBZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpzV8NE8s7067ZLWyi1jRvJklJnlBFEUyq1al9AqaQ7pI4DcRJq_Lf3JCtFMXgpPQyk/copeland-park-bar-peckham',
                   location='Peckham',
                   has_sockets=1,
                   has_toilet=1,
                   has_wifi=1,
                   can_take_calls=0,
                   seats='20-30',
                   coffee_price='£2.75'
                   )
    newcafe3 = Cafe(id=3, name='One & All Cafe Peckham',
                   map_url='https://g.page/one-all-cafe?share',
                   img_url='https://lh3.googleusercontent.com/p/AF1QipOMzXpKAQNyUvrjTGHqCgWk8spwnzwP8Ml2aDKt=s0',
                   location='Peckham',
                   has_sockets=1,
                   has_toilet=1,
                   has_wifi=1,
                   can_take_calls=0,
                   seats='20-30',
                   coffee_price='£2.75'
                   )
    db.session.add(newcafe)
    db.session.add(newcafe1)
    db.session.add(newcafe3)
    db.session.commit()
except:
    print('no')
    pass

@app.route("/")
def home():
    """the landing page which displays a link to the documentation for the cafes API"""
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def random_cafe():
    """request a random cafe from the database

    GET: request a random cafe from the database in json format
    """
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    # random_cafe_dictionary = {
    #     'can_take_calls': random_cafe.can_take_calls,
    #     'coffee_price': random_cafe.coffee_price,
    #     'has_sockets': random_cafe.has_sockets,
    #     'has_toilet': random_cafe.has_toilet,
    #     'has_wifi': random_cafe.has_wifi,
    #     'id': random_cafe.id,
    #     'img_url': random_cafe.img_url,
    #     'location': random_cafe.location,
    #     'map_url': random_cafe.map_url,
    #     'name': random_cafe.name,
    #     'seats': random_cafe.seats
    # }
    return jsonify(cafe=random_cafe.to_dict())

@app.route('/all', methods=['GET'])
def all_cafes():
    """request all the cafes in the database

    GET: request all the cafes in the database, returned in json as a list of dictionaries

    Returns
    -------
        all the cafes in the database, returned in json as a list of dictionaries
    """
    all_cafes = Cafe.query.all()
    all_cafes_list = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes_list)

@app.route('/search', methods=['GET'])
def search_cafes():
    """search for a specific cafe in the database based on location

    GET: search for a specific cafe in the database based on location, if no matches are found, returns an error
         message in json. All matches are return in json as a list of dictionaries

    Returns
    -------
        all the cafes that match the location to search for
    """
    location = request.args.get('loc')
    matched_cafes = Cafe.query.filter_by(location=location).all()
    if len(matched_cafes) == 0:
        not_found_dictionary = {
            'Not Found': 'Sorry, we don\'t have a cafe at that location'
        }
        return jsonify(error=not_found_dictionary)
    matched_cafes_list = [cafe.to_dict() for cafe in matched_cafes]
    return jsonify(cafes=matched_cafes_list)


## HTTP POST - Create Record

@app.route('/add', methods=['POST'])
def add():
    """add a new cafe to the database

    POST: add a new cafe to the database, returns a success message in json if successful

    Returns
    -------
        a json file to indicate the cafe was successfully added to the database
    """
    new_cafe = Cafe(name=request.form['name'],
                    map_url=request.form['map_url'],
                    img_url=request.form['img_url'],
                    location=request.form['location'],
                    seats=request.form['seats'],
                    has_toilet=(request.form['has_toilet'] == 'True'),
                    has_wifi=(request.form['has_wifi'] == 'True'),
                    has_sockets=(request.form['has_sockets'] == 'True'),
                    can_take_calls=(request.form['can_take_calls'] == 'True'),
                    coffee_price=request.form['coffee_price']
                    )
    db.session.add(new_cafe)
    db.session.commit()
    success_dictionary = {
        'success': 'Successfully added a new cafe to the database.'
    }
    return jsonify(response=success_dictionary)


## HTTP PUT/PATCH - Update Record
@app.route('/update_price/<int:id>', methods=['PATCH'])
def update_price(id):
    """update the price of a cafe in the database

    PATCH: update the price of a cafe in the database

    Parameters
    ----------
    id: int
        the id of the cafe the user wishes to update the price for

    Returns
    -------
        a json message to indicate of the cafe was successfully update in the database
    """
    new_price = request.args.get('new_price')
    specified_cafe = Cafe.query.get(id)
    if specified_cafe is None:
        return jsonify(error={'Not Found': 'Sorry a cafe with that id was not found in the database'}), 404
    specified_cafe.coffee_price = new_price
    db.session.commit()
    return jsonify(success='Successfully updated the price.'), 200




## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:id>', methods=['DELETE'])
def report_closed(id):
    """deletes the specified cafe from the database if the api_key matches the top_secret_key

    DELETE: deletes the specified cafe from the database

    Parameters
    ----------
    id: int
        the id of the cafe to delete in the database

    Returns
    -------
        a json message indicating the outcome of the DELETE request
    """
    cafe_id = id
    #top_secret_key = 'password'
    top_secret_key = os.environ.get('top_secret_key') # heroku config var
    api_key = request.args.get('api_key')
    if api_key != top_secret_key:
        return jsonify(error='Sorry, that\'s not allowed. Make sure you have the correct api_key.'), 403
    specified_cafe = Cafe.query.get(cafe_id)
    if specified_cafe:
        db.session.delete(specified_cafe)
        db.session.commit()
        return jsonify(success='The cafe was deleted'), 200
    else:
        return jsonify(error={'Not Found':'Sorry a cafe with that id was not found in the database.'}), 404




if __name__ == '__main__':
    app.run(debug=True)
