from flask import Blueprint

users = Blueprint('users', __name__, url_prefix="/users")
sessions = Blueprint('sessions', __name__, url_prefix="/sessions")
projects = Blueprint('projects', __name__, url_prefix="/projects")
notifications = Blueprint('notifications', __name__, url_prefix="/notifications")
events = Blueprint('events', __name__, url_prefix="/events")

from routes.users import *
from routes.sessions import *
from routes.projects import *
from routes.notifications import *
from routes.events import*
