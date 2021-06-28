from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from os import environ
from uuid import uuid4
from functools import wraps
from flask import request, redirect, url_for
from models.storage import DB
from routes import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


DB_MIGRATION_URI = DB._MySQLClient__engine.url


# initialize the app
app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())
CORS(app, resources={r"*": {"origins": "*"}})


app.config["SQLALCHEMY_DATABASE_URI"] = DB_MIGRATION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.register_blueprint(users)



@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({
        'status': 'OK'
    }), 200

# handle errors (abort)
@app.errorhandler(400)
def bad_request(error) -> str:
    return jsonify({"error": "Bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(403)
def Forbidden(error) -> str:
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(401)
def Unauthorized(error) -> str:
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
