from flask import Flask
from models.storage import DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

DB_MIGRATION_URI = DB._MySQLClient__engine.url

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_MIGRATION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from models.base import Base
from uuid import uuid4


def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))


class User(Base, db.Model):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)
    projects = Column(String(256), nullable=True)
    # TODO: We should make these nullable=False. See Issue #67
    credits = Column(Integer(), nullable=False)
    access_token = Column(String(128))

    # * If you get another failure, Russ, save the error msg and share it on
    # * issue #68, then uncomment the old str(uuid4())'s and try again
    # TODO: See Issue #68
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = kwargs.get('id') # or str(uuid4())
        self.email = kwargs.get('email') # or str(uuid4())
        self.name = kwargs.get('name') or kwargs.get('login') # or str(uuid4())
        self.handle = kwargs.get('login')
        self.avatar_url = kwargs.get('avatar_url')
        self.access_token = kwargs.get('access_token')
        self.projects = kwargs.get('projects')
        self.credits = 0


class Session(Base, db.Model):
    __tablename__ = 'sessions'
    user_id = Column(String(128), nullable=False)
    created_at = Column(String(64), nullable=False)
    id = Column(String(60), nullable=False, primary_key=True)

    def __init__(self, token, user_id):
        super().__init__()
        self.id = token
        self.user_id = user_id

class Token(Base, db.Model):
    __tablename__ = 'api_tokens'
    id = Column(String(128), nullable=False, primary_key=True)
    user_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, user_name, email):
        super().__init__()
        self.id = str(uuid4())
        self.user_name = user_name
        self.email = email # or str(uuid4())

class LearningResource(Base, db.Model):
    __tablename__ = 'learn_resources'
    # PARENTS ------------------------------------------------
    # which type of project this belongs to String(128), ForeignKey('project_templates.id')
    project_template_id = to_one('project_templates.id', String, 128)
    # which type of sprint this belongs to
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # which type of task this belongs to
    task_template_id = to_one('task_templates.id', String, 128)
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    articles = Column(String(128))
    videos = Column(String(128))
    external_links = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.articles = kwargs.get('articles')
            self.videos = kwargs.get('videos')
            self.external_links = kwargs.get('external_links')



class ProjectTemplate(Base, db.Model):
    __tablename__ = 'project_templates'
    # CHILDREN -----------------------------------------------
    # so we can find all of a given type of project users made
    projects = to_many("Project", "project_templates")
    # so we know what sprint types are associated with this project type
    sprint_templates = to_many("SprintTemplate", "project_templates")
    # learning resources for this at the project level
    learning_resources = to_many("LearningResource", "project_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    name = Column(String(128))
    link = Column(String(128))
    author = Column(String(128))
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    quiz = Column(String(128))
    preview_images = Column(String(128))
    cost = Column(Integer)
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.name = kwargs.get('name')
            self.link = kwargs.get('link')
            self.author = kwargs.get('author')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.quiz = kwargs.get('quiz') # quiz table
            self.preview_images = kwargs.get('preview_images')
            self.cost = 5
            


class Project(Base, db.Model):
    __tablename__ = 'projects'
    # PARENTS ------------------------------------------------
    # which type of project this is
    project_template_id = to_one('project_templates.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # the actual sprints the user works on in this project
    sprints = to_many("Sprint", "projects")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=True)
    repository_link = Column(String(128), nullable=True)
    progress = Column(String(128))
    quiz_status = Column(String(128))
    roles = Column(String(128), nullable=True)   
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = str(uuid4())
            self.name = kwargs.get('name')
            self.repository_link = kwargs.get('repository_link')
            self.progress = kwargs.get('progress')
            self.quiz_status = kwargs.get('quiz_status')
            self.roles = kwargs.get('roles')
            

class SprintTemplate(Base, db.Model):
    __tablename__ = 'sprint_templates'
    # PARENTS ------------------------------------------------
    # which type of project this is in
    project_template_id = to_one('project_templates.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # which actual sprints of this type are being worked on by users
    sprints = to_many("Sprint", "sprint_templates")
    # which type of tasks this has in it
    task_templates = to_many("TaskTemplate", "sprint_templates")
    # learning resources for this at the sprint level
    learning_resources = to_many("LearningResource", "sprint_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    number = Column(Integer)
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    quiz = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.number = kwargs.get('number')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.quiz = kwargs.get('quiz') # quiz table

class Sprint(Base, db.Model):
    __tablename__ = 'sprints'
    # PARENTS ------------------------------------------------
    # which type of sprint this is in
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # which actual project this is part of
    project_id = to_one('projects.id', String, 128) 
    # CHILDREN -----------------------------------------------
    # which actual tasks it has in it
    tasks = to_many("Task", "sprints")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    progress = Column(String(128))
    quiz_status = Column(String(128))
    roles = Column(String(128))   
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.progress = kwargs.get('progress')
            self.quiz_status = kwargs.get('quiz_status')
            self.roles = kwargs.get('roles')


class TaskTemplate(Base, db.Model):
    __tablename__ = 'task_templates'
    # PARENTS ------------------------------------------------
    # which type of sprint this is in
    sprint_template_id = to_one('sprint_templates.id', String, 128)
    # CHILDREN -----------------------------------------------
    # which actual tasks it has in it
    tasks = to_many("Task", "task_templates")
    # learning resources for this at the task level
    learning_resources = to_many("LearningResource", "task_templates")
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    number = Column(Integer)
    tech_dependencies = Column(String(128))
    role_types = Column(String(128))
    description = Column(String(256))
    goals = Column(String(128))
    tests = Column(String(128))
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.number = kwargs.get('number')
            self.tech_dependencies = kwargs.get('tech_dependencies')
            self.role_types = kwargs.get('role_types') # list of titles?
            self.description = kwargs.get('description')
            self.goals = kwargs.get('goals')
            self.tests = kwargs.get('tests') # quiz table

class Task(Base, db.Model):
    __tablename__ = 'tasks'
    # PARENTS ------------------------------------------------
    # which type of task this is
    task_template_id = to_one('task_templates.id', String, 128)
    # which actual sprint this is in
    sprint_id = to_one('sprints.id', String, 128)
    # --------------------------------------------------------
    id = Column(String(128), primary_key=True)
    status = Column(String(128))   
    role = Column(String(128))  
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') or str(uuid4())
            self.status = kwargs.get('status')
            self.role = kwargs.get('role')



