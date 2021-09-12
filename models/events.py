
from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql.expression import null
from models.base import declarative_base, Base
from uuid import uuid4

class Event(Base, declarative_base):
    __tablename__ = 'events'
    id = Column(String(128), primary_key=True)
    message = Column(String(512), nullable=False)
    user_handle = Column(String(128), nullable=True)
    user_link = Column(String(128), nullable=True)
    sprint_name = Column(String(128), nullable=True)
    sprint_link = Column(String(128), nullable=True)
    project_name = Column(String(128), nullable=True)
    project_link = Column(String(128), nullable=True)
    type = Column(String(128), nullable=True)


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = str(uuid4())
        self.user_handle = kwargs.get('user_handle')
        self.user_link = kwargs.get('user_link')
        self.sprint_name = kwargs.get('sprint_name')
        self.sprint_link = kwargs.get('sprint_link')
        self.project_name = kwargs.get('project_name')
        self.project_link = kwargs.get('project_link')
        self.type = kwargs.get('type')
        self.message = self.build_message(kwargs)
    
    @staticmethod
    def build_message(kwargs):
        type = kwargs.get('type')
        if type == 'PROJECT_STARTED':
            user_handle = kwargs.get('user_handle')
            user_link = kwargs.get('user_link')
            project_name = kwargs.get('project_name')
            project_link = kwargs.get('project_link')
            return f'<a class="event_user_handle" href="{user_link}">{user_handle}</a> created a new project, <a class="event_project_name" href="{project_link}">{project_name}</a>'
