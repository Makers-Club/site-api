from flask import Blueprint

users = Blueprint('users', __name__, url_prefix="/users")
sessions = Blueprint('sessions', __name__, url_prefix="/sessions")
learning_resources = Blueprint('learning_resources', __name__, url_prefix="/learning_resources")
project_templates = Blueprint('project_templates', __name__, url_prefix="/project_templates")
projects = Blueprint('projects', __name__, url_prefix="/projects")
sprint_templates = Blueprint('sprint_templates', __name__, url_prefix="/sprint_templates")
sprints = Blueprint('sprints', __name__, url_prefix="/sprints")
task_templates = Blueprint('task_templates', __name__, url_prefix="/task_templates")
tasks = Blueprint('tasks', __name__, url_prefix="/tasks")


from routes.users import *
from routes.sessions import *
from routes.projects import *
