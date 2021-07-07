from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

class User(Base, declarative_base):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)
    # TODO: We should make these nullable=False. See Issue #67
    credits = Column(Integer())
    access_token = Column(String(128))

    # * If you get another failure, Russ, save the error msg and share it on
    # * issue #68, then uncomment the old str(uuid4())'s and try again
    # TODO: See Issue #68
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs:
            print(kwargs, '\nHEYHEYEHEYEHEYEHEYE\n')
            self.id = kwargs.get('id')
            self.email = kwargs.get('email')
            self.name = kwargs.get('name') or kwargs.get('login')
            self.handle = kwargs.get('login') or kwargs.get('handle')
            self.avatar_url = kwargs.get('avatar_url')
            self.access_token = kwargs.get('access_token')
            self.credits = kwargs.get('credits') or 0

        
