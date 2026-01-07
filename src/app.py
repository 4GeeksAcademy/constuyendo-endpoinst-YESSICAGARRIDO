"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Film, Planet, Vehicle, Favoritefilm, Peoplefavorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def user():
    all_user = User.query.all()
    all_users = [user.serialize()for user in all_user]

    return jsonify(all_users), 200


@app.route('/people', methods=['GET'])
def get_people():

    all_people = People.query.all()
    all_people = list(map(lambda p: p.serialize(), all_people))

    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    people = People.query.get(people_id)
    if people is None:
        return jsonify({"message": "People not found"}), 404

    return jsonify(people.serialize()), 200


@app.route('/film', methods=['GET'])
def get_film():

    all_film = Film.query.all()
    all_film = list(map(lambda f: f.serialize(), all_film))

    return jsonify(all_film), 200


@app.route('/film/<int:film_id>', methods=['GET'])
def get_film_id(film_id):

    film = Film.query.get(film_id)
    if film is None:
        return jsonify({"message": "Film not found"}), 404

    return jsonify(film.serialize()), 200


@app.route('/planet', methods=['GET'])
def get_planet():

    all_planet = Planet.query.all()
    all_planet = list(map(lambda f: f.serialize(), all_planet))

    return jsonify(all_planet), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/vehicle', methods=['GET'])
def get_vehicle():

    all_vehicle = Vehicle.query.all()
    all_vehicle = list(map(lambda f: f.serialize(), all_vehicle))

    return jsonify(all_vehicle), 200


@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_id(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    return jsonify(vehicle.serialize()), 200


@app.route('/user/favorite', methods=['GET'])
def get_user_favorite():

    user = User.query.get()

    people_favorite = [f.people.serialize()
                       for f in user.people_favorite]
    favorite_film = [f.film.serialize()
                     for f in user.favorite_film]

    return jsonify({
        "user_id": user.id,
        "favorite": {
            "people": people_favorite,
            "film": favorite_film
        }}), 200


@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(user_id, people_id):
     
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    
    favorite = Peoplefavorite(user_id=user_id, people_id=people_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "People added"}), 201


@app.route('/user/<int:user_id>/favorite/film/<int:film_id>', methods=['POST'])
def add_film_favorite(user_id, film_id):
     
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite = Favoritefilm(user_id=user_id, film_id=film_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Film added"}), 201


@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite = Peoplefavorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "favorite remove"}), 200

   

@app.route('/user/<int:user_id>/favorite/film/<int:film_id>', methods=['DELETE'])
def delete_favorite_film(user_id, film_id):

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite = Favoritefilm.query.filter_by(
        user_id=user_id, film_id=film_id).first()
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "favorite remove"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
