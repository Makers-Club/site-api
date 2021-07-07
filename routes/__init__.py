from flask import Blueprint

users = Blueprint('users', __name__, url_prefix="/users")
sessions = Blueprint('sessions', __name__, url_prefix="/sessions")
projects = Blueprint('projects', __name__, url_prefix="/projects")


from routes.users import *
from routes.sessions import *
from routes.projects import *
