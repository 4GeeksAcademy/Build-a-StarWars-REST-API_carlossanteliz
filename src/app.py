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
from models import db, User
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
# ////////
# trayendo a todos lo usuarios


@app.route('/users', methods=['GET'])
def all_users():
    try:

        query_results = User.query.all()

        if not query_results:
            return jsonify({"msg": "Usuarios no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "Todo salió bien",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

# trayendo un usario por ID


@app.route('/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    try:

        query_results = User.query.filter_by(id=user_id).first()

        if not query_results:
            return jsonify({"msg": "Usuario no existente"}), 400

        response_body = {
            "msg": "usuario encontrado",
            "results": query_results.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}, 500)


@app.route('/users/favorites', methods=['GET'])
def all_users_favorites():
    try:
        current_user = User.query.first()

        if not current_user:
            return jsonify({"msg": "Usuario actual no encontrado"}), 400

        favorites = Favorite.query.filter_by(user_id=current_user.id).all()

        results = list(map(lambda item: serialize(), favorites))

        response_body = {
            "msg": "Todo salió bien",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener favoritos del ususaio: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/people', methods=['GET'])
def all_people():
    try:
        query_results = People.query.all()

        if not query_results:
            return jsonify({"msg": "Personas no encontradas"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "Todo salió bien",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener personas: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}, 500)


@app.route('/people/<int:people_id>', methods=['GET'])
def person_by_id(people_id):
    try:
        query_results = People.query.filter_by(id=people_id).first()

        if not query_results:
            return jsonify({"msg": "Persona no existente"}), 400

        response_body = {
            "msg": "Persona encontrada",
            "results": "query_results.serialize()"
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener persona: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/planets', methods=['GET'])
def all_planets():
    try:
        query_results = Planets.query.all()

        if not query_results:
            return jsonify({"msg": "Planetas no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "Todo salió bien",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener planetas: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_by_id(planet_id):
    try:
        query_results = Planet.query.filter_by(id=planet_id).first()

        if not query_results:
            return jsonify({"msg": "Planeta no existente"}), 400

        response_body = {
            "msg": "Planeta encontrado",
            "results": query_results.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al obtener planeta: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        current_user = User.query.first()

        if not current_user:
            return jsonify({"msg": "Usuario actual no encontrado"}), 400

        planet = Planet.query.filter_by(id=planet_id).first()
        if not planet:
            return jsonify({"msg": "Planeta no existente"}), 400

        existing = Favorite.query.filter_by(
            user_id=current_user.id, planet_id=planet_id).first()
        if existing:
            return jsonify({"msg": "Favorito de planeta ya existe", "results": existing.serialize()}), 200

        fav = Favorite(user_id=current_user.id, planet_id=planet_id)
        db.session.add(fav)
        db.session.commit()

        response_body = {
            "msg": "Favorito de planeta agregado",
            "results": fav.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al agregar favorito de planeta: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        current_user = User.query.first()

        if not current_user:
            return jsonify({"msg": "Usuario actual no encontrado"}), 400

        person = People.query.filter_by(id=people_id).first()
        if not person:
            return jsonify({"msg": "Persona no existente"}), 400

        existing = Favorite.query.filter_by(
            user_id=current_user.id, people_id=people_id).first()
        if existing:
            return jsonify({"msg": "Favorito de persona ya existe", "results": existing.serialize()}), 200

        fav = Favorite(user_id=current_user.id, people_id=people_id)
        db.session.add(fav)
        db.session.commit()

        response_body = {
            "msg": "Favorito de persona agregado",
            "results": fav.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al agregar favorito de persona: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        current_user = User.query.first()

        if not current_user:
            return jsonify({"msg": "Usuario actual no encontrado"}), 400

        fav = Favorite.query.filter_by(
            user_id=current_user.id, planet_id=planet_id).first()
        if not fav:
            return jsonify({"msg": "Favorito de planeta no existente"}), 400

        db.session.delete(fav)
        db.session.commit()

        response_body = {
            "msg": "Favorito de planeta eliminado",
            "results": {"planet_id": planet_id}
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al eliminar favorito de planeta: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        current_user = User.query.first()

        if not current_user:
            return jsonify({"msg": "Usuario actual no encontrado"}), 400

        fav = Favorite.query.filter_by(
            user_id=current_user.id, people_id=people_id).first()
        if not fav:
            return jsonify({"msg": "Favorito de persona no existente"}), 400

        db.session.delete(fav)
        db.session.commit()

        response_body = {
            "msg": "Favorito de persona eliminado",
            "results": {"people_id": people_id}
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error al eliminar favorito de persona: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
