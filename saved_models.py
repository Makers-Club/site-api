from flask import Flask
from models.storage import DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB_MIGRATION_URI = DB._MySQLClient__engine.url

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_MIGRATION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4


class User(Base, db.Model):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)
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


class Project(Base, db.Model):
    __tablename__ = 'projects'
    id = Column(String(128), nullable=False, primary_key=True)
    title = Column(String(128), nullable=False)
    repository = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    preview_images = Column(String(128), nullable=False)
    videos = Column(String(128), nullable=False)
    resources = Column(String(128), nullable=False)
    quizzes = Column(String(128), nullable=False)
    goals = Column(String(128), nullable=False)
    dependencies = Column(String(128), nullable=False)
    progress = Column(String(128), nullable=False)
    sprints = Column(String(128), nullable=False)
    cost = Column(Integer)

    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            self.id = kwargs.get('id') # or str(uuid4())
            self.title = kwargs.get('title')
            self.repository = kwargs.get('repository')
            self.description = kwargs.get('description')
            self.preview_images = kwargs.get('preview_images')
            self.videos = kwargs.get('videos')
            self.resources = kwargs.get('resources')
            self.quizzes = kwargs.get('quizzes')
            self.goals = kwargs.get('goals')
            self.dependencies = kwargs.get('dependencies')
            self.progress = kwargs.get('progress')
            self.sprints = kwargs.get('sprints')
            self.cost = kwargs.get('cost')
