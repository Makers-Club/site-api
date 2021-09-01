from sqlalchemy import Column, String, Float, Integer
from models.base import Base, declarative_base
from uuid import uuid4

class Token(Base, declarative_base):
    __tablename__ = 'api_tokens'
    client_id = Column(String(128), nullable=False, primary_key=True)
    id = Column(String(128), nullable=False)
    permission = Column(String(60))

    def __init__(self, client_id, access_token, permission=None):
        super().__init__()
        self.client_id = client_id
        self.id = access_token
        self.permission = permission or 'user'
