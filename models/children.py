from sqlalchemy import Column, String, Float, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

class Parent(Base, declarative_base):
    __tablename__ = 'parent'
    id = Column(String(128), primary_key=True)
    children = relationship("Child", backref="parent")

    def __init__(self, *args, **kwargs):
        super().__init__()  
        self.id = str(uuid4())

class Child(Base, declarative_base):
    __tablename__ = 'child'
    id = Column(String(128), primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

    def __init__(self, *args, **kwargs):
        super().__init__() 
        self.id = str(uuid4())