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
from models import db, User, People, Planet, Starship, FavoritePeople, FavoritePlanets, FavoriteStarships
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


# USER


@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'email' not in body:
        return jsonify({"msg": "Debe enviar el correo electrónico"}), 400
    if 'password' not in body:
        return jsonify({"msg": "Debe enviar la contraseña"}), 400
    if 'username' not in body:
        return jsonify({"msg": "Debe enviar el nombre de usuario"}), 400
    
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.username = body['username']
    new_user.name = body['name']
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado exitosamente"}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'data': users_serialized}), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no existe"}), 404

    return jsonify({
        "people": [fav.people.serialize() for fav in user.favorite_people],
        "starships": [fav.starship.serialize() for fav in user.favorite_starships],
        "planets": [fav.planet.serialize() for fav in user.favorite_planets]
        
    }), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado exitosamente"}), 200


# PEOPLE

@app.route('/people', methods=['POST'])
def add_people():  # la informacion viene en el body de la request
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre del personaje"}), 400
    if 'gender' not in body:
        return jsonify({"msg": "Es obligatorio el género del personaje"}), 400
    if 'height' not in body:
        return jsonify({"msg": "Es obligatorio  la altura del personaje"}), 400
    

    new_people = People()
    new_people.name = body['name']
    new_people.gender = body['gender']
    new_people.height = body['height']

    db.session.add(new_people)
    db.session.commit()

    return jsonify({"msg": "Personaje agregado exitosamente"}), 201


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([pe.serialize() for pe in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.get(1)
    person = People.query.get(people_id)

    if not person:
        return jsonify({"msg": "Personaje no existe"}), 404

    fav = FavoritePeople(user_id=user.id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Personaje agregado a favoritos"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    fav = FavoritePeople.query.filter_by(
        user_id=1, people_id=people_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Favorito eliminado"}), 200

# Starship
@app.route('/starships', methods=['POST'])
def add_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre de la nave"}), 400
    if 'cost_in_credits' not in body:
        return jsonify({"msg": "Es obligatorio el coste en créditos de la nave"}), 400
    if 'speed' not in body:
        return jsonify({"msg": "Es obligatoria la velocidad de la nave"}), 400

    new_starship = Starship()
    new_starship.name = body['name']
    new_starship.cost_in_credits = body['cost_in_credits']
    new_starship.speed = body['speed']
    
    db.session.add(new_starship)
    db.session.commit()

    return jsonify({"msg": "Nave agregada exitosamente"}), 201


@app.route('/starships/', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([v.serialize() for v in starships]), 200


@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"msg": "Nave no encontrada"}), 404
    return jsonify(starship.serialize()), 200


@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id):
    user = User.query.get(1)
    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({"msg": "Nave no existe"}), 404

    fav = FavoriteStarships(user_id=user.id, starship_id=starship_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Nave agregada a favoritos"}), 201


@app.route('/favorite/ship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    fav = FavoriteStarships.query.filter_by(
        user_id=1, starship_id=starship_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200


# PLANETS

@app.route("/planets/", methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre del planeta"}), 400
    if 'size' not in body:
        return jsonify({"msg": "Es obligatorio el tamaño del planeta"}), 400
    if 'population' not in body:
        return jsonify({"msg": "Es obligatoria la población del planeta"}), 400
    if 'climate' not in body:
        return jsonify({"msg": "Es obligatorio el clima del planeta"}), 400
    

    new_planet = Planet()
    new_planet.name = body['name']
    new_planet.size = body['size']
    new_planet.population = body['population']
    new_planet.climate = body['climate']

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado exitosamente"}), 201


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(1)
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planeta no existe"}), 404

    fav = FavoritePlanets(user_id=user.id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado a favoritos"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = FavoritePlanets.query.filter_by(
        user_id=1, planet_id=planet_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Vehículo eliminado de favoritos"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
