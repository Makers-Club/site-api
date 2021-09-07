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

from sqlalchemy import Column, String, Float, Integer, Table, Boolean
from sqlalchemy.orm import relationship
from models.base import Base
from uuid import uuid4


def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))

users_and_projects = Table('association', db.Model.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('projects_id', ForeignKey('projects.id'), primary_key=True)
)
    

'''

class Team(Base, db.Model):
    __tablename__ = 'teams'
    name = Column(String(128), nullable=False)
    id = Column(String(128), primary_key=True)
    # Children - to many relationships
    users = to_many("User", "teams")

class Role(Base, db.Model):
    __tablename__ = 'roles'
    name = Column(String(128), nullable=False)
    id = Column(String(128), primary_key=True)
'''

class User(Base, db.Model):
    __tablename__ = 'users'
    id = Column(String(128), primary_key=True)
    email = Column(String(128), nullable=True)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)
    credits = Column(Integer(), nullable=False)
    access_token = Column(String(128))
    # Children - to many relationships
    my_projects = relationship(
        "Project",
        secondary=users_and_projects,
        back_populates="my_users")
    #teams = to_many("Team", "users")
    #roles_seeking = to_many("Role", "users")
    interests = Column(String(256), nullable=True)
    about_me = Column(String(256), nullable=True)
    culture = Column(String(256), nullable=True)
    title = Column(String(256), nullable=True)
    roles_of_interest = Column(String(256), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = kwargs.get('id') # or str(uuid4())
        self.email = kwargs.get('email') # or str(uuid4())
        self.name = kwargs.get('name') or kwargs.get('login') # or str(uuid4())
        self.handle = kwargs.get('login')
        self.avatar_url = kwargs.get('avatar_url')
        self.access_token = kwargs.get('access_token')
        self.credits = 0
        self.interests = kwargs.get('interests')
        self.about_me = kwargs.get('about_me')
        self.culture = kwargs.get('culture')
        self.title = kwargs.get('title')
        self.roles_of_interest = kwargs.get('roles_of_interest')


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
    client_id = Column(String(128), nullable=False, primary_key=True)
    id = Column(String(128), nullable=False)
    permission = Column(String(60))

    def __init__(self, client_id, access_token, permission=None):
        super().__init__()
        self.client_id = client_id
        self.id = access_token
        self.permission = permission or 'user'

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
    # MANY TO MANY
    my_users = relationship(
        "User",
        secondary=users_and_projects,
        back_populates="my_projects")
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


class Notification(Base, db.Model):
    __tablename__ = 'notifications'
    id = Column(String(128), primary_key=True)
    user_id = Column(String(128), nullable=False)
    msg = Column(String(256), nullable=False)
    is_read = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = kwargs.get('id') # or str(uuid4())
        self.user_id = kwargs.get('user_id') # or str(uuid4())
        self.msg = kwargs.get('msg')
        self.is_read = kwargs.get('is_read')