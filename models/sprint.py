from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4


def to_many(child_class_name, this_table_name):
    return relationship(child_class_name, backref=this_table_name)

def to_one(parent_dot_id_str, data_type, len=None):
    return Column(data_type(len), ForeignKey(parent_dot_id_str))

sprints_and_users = Table('sprints_and_users', declarative_base.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('sprints_id', ForeignKey('sprints.id'), primary_key=True)
)


class Sprint(Base, declarative_base):
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
        if kwargs:
            print('\nSPRINT KWARGS\n\t', kwargs, '\n')
            self.description = kwargs.get('description')
            self.progress = 0
            self.project_id = kwargs.get('project_id')