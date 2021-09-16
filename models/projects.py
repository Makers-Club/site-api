from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from models.base import declarative_base, Base
from uuid import uuid4

def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))

'''users_and_projects = Table('association', declarative_base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('project_id', ForeignKey('projects.id'), primary_key=True)
)'''
from models.user import users_and_projects

   

class Project(Base, declarative_base):
    __tablename__ = 'projects'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=True)
    repository_link = Column(String(128), nullable=True)
    repository_name = Column(String(128), nullable=True)
    owner_handle = Column(String(128), nullable=True)
    user_pic = Column(String(128), nullable=True)
    my_users = relationship(
        "User",
        secondary=users_and_projects,
        back_populates="my_projects") 
    complete = Column(Integer, nullable=False)
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.id = str(uuid4())
        if kwargs:
            print(kwargs)
            self.name = kwargs.get('name')
            self.repository_link = kwargs.get('repository_link')
            self.repository_name = kwargs.get('repository_name')
            self.owner_handle = kwargs.get('owner_handle')
            self.user_pic = kwargs.get('user_pic')
            self.complete = 0
        else:
            print(args.get('name'))
    

