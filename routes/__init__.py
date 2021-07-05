from flask import Blueprint

users = Blueprint('users', __name__, url_prefix="/users")
sessions = Blueprint('sessions', __name__, url_prefix="/sessions")


from routes.users import *
from routes.sessions import *
