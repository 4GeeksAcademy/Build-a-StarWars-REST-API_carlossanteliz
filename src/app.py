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


@app.route('/user', methods=['GET'])
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
    
#trayendo un usario por ID
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





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
