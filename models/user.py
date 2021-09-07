from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))

users_and_projects = Table('association', declarative_base.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('projects_id', ForeignKey('projects.id'), primary_key=True)
)

class User(Base, declarative_base):
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


        
