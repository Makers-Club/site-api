
from sqlalchemy import Column, String, Boolean
from models.base import declarative_base, Base

class Events(Base, declarative_base):
    __tablename__ = 'events'
    id = Column(String(128), primary_key=True)
    user_handle = Column(String(128), nullable=True)
    user_link = Column(String(128), nullable=True)
    sprint_name = Column(String(128), nullable=True)
    sprint_link = Column(String(128), nullable=True)
    project_name = Column(String(128), nullable=True)
    project_link = Column(String(128), nullable=True)
    type = Column(String(128), nullable=True)


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = kwargs.get('id')
        self.user_handle = kwargs.get('user_handle')
        self.user_link = kwargs.get('user_link')
        self.sprint_name = kwargs.get('sprint_name')
        self.sprint_link = kwargs.get('sprint_link')
        self.project_name = kwargs.get('project_name')
        self.project_link = kwargs.get('project_link')
        self.message = kwargs.get('message')
        self.type = kwargs.get('type')