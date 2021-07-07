from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

class Project(Base, declarative_base):
    __tablename__ = 'projects'
    id = Column(String(128), nullable=False, primary_key=True)
    title = Column(String(128), nullable=False)
    repository = Column(String(128), nullable=False)
    description = Column(String(128))
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

