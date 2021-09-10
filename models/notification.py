from sqlalchemy import Column, String, Boolean
from models.base import declarative_base, Base

class Notification(Base, declarative_base):
    __tablename__ = 'notifications'
    id = Column(String(128), primary_key=True)
    user_id = Column(String(128), nullable=False)
    msg = Column(String(256), nullable=False)
    is_read = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user_id = kwargs.get('user_id') # or str(uuid4())
        self.msg = kwargs.get('msg')
        self.is_read = kwargs.get('is_read')
