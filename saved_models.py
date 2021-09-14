import uuid
from uuid import uuid4
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

from models.sprint import sprints_and_users


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
    my_sprints = relationship(
        "Sprint",
        secondary=sprints_and_users,
        back_populates="participants")
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



class Project(Base, db.Model):
    __tablename__ = 'projects'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=True)
    repository_link = Column(String(128), nullable=True)
    repository_name = Column(String(128), nullable=True)
    owner_handle = Column(String(128), nullable=True)   
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = str(uuid4())
        self.name = kwargs.get('name')
        self.repository_link = kwargs.get('repository_link')
        self.repository_name = kwargs.get('repository_name')
        self.owner_handle = kwargs.get('owner_handle')
    



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


class Event(Base, db.Model):
    __tablename__ = 'events'
    id = Column(String(128), primary_key=True)
    message = Column(String(512), nullable=False)
    user_handle = Column(String(128), nullable=True)
    user_link = Column(String(128), nullable=True)
    sprint_number = Column(String(128), nullable=True)
    sprint_link = Column(String(128), nullable=True)
    project_name = Column(String(128), nullable=True)
    project_link = Column(String(128), nullable=True)
    type = Column(String(128), nullable=True)


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = str(uuid4())
        self.user_handle = kwargs.get('user_handle')
        self.user_link = kwargs.get('user_link')
        self.sprint_number = kwargs.get('sprint_number')
        self.sprint_link = kwargs.get('sprint_link')
        self.project_name = kwargs.get('project_name')
        self.project_link = kwargs.get('project_link')
        self.type = kwargs.get('type')
        self.message = self.build_message(kwargs)

    @staticmethod
    def build_message(kwargs):
        msg_type = kwargs.get('type')
        if msg_type == 'PROJECT_STARTED':
            user_handle = kwargs.get('user_handle')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            return f'<a class="event_user_handle" href="/users/{user_handle}">{user_handle}</a> created a new project, <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'SPRINT_STARTED':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            sprint_number = kwargs.get('sprint_number')
            sprint_link = kwargs.get('sprint_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            return f'<a class="event_user_handle" href="/users/{user_handle}">{user_handle}</a> started <a class="event_sprint_number" href="{sprint_link}">Sprint {sprint_number}</a> of <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'NEW_USER':
            user_handle = kwargs.get('user_handle')
            return f'<a class="event_user_handle" href="/users/{user_handle}">{user_handle}</a> joined Maker Teams! Welcome them.'
        if msg_type == 'JOINED_SPRINT':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            sprint_number = kwargs.get('sprint_number')
            sprint_link = kwargs.get('sprint_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            return f'<a class="event_user_handle" href="/users/{user_handle}">{user_handle}</a> joined <a class="event_sprint_number" href="{sprint_link}">Sprint {sprint_number}</a> of <a class="event_project_name" href="{project_link}">{project_name}</a>'
        if msg_type == 'GAVE_PROJECT_FEEDBACK':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            return f'<a class="event_user_handle" href="/users/{user_handle}">{user_handle}</a> gave feedback on <a class="event_project_name" href="{project_link}">{project_name}</a>'


sprints_and_users = Table('sprints_and_users', db.Model.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('sprints_id', ForeignKey('sprints.id'), primary_key=True)
)

class Sprint(Base, db.Model):
    __tablename__ = 'sprints'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    description = Column(String(128))
    progress = Column(String(128), nullable=False)
    project_id = Column(String(128), ForeignKey('projects.id'))
    participants = relationship(
        "User",
        secondary=sprints_and_users,
        back_populates="my_sprints")

    def __init__(self, *args, **kwargs):
        super().__init__()  
        del self.id
        if kwargs:
            self.description = kwargs.get('description')
            self.progress = 0
            self.project_id = kwargs.get('project')