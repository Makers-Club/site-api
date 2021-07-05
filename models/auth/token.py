from sqlalchemy import Column, String, Float, Integer
from models.base import Base
from uuid import uuid4

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
