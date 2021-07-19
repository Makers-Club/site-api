from sqlalchemy import Column, String
from models.base import declarative_base, Base

class Session(Base, declarative_base):
    __tablename__ = 'sessions'
    user_id = Column(String(128), nullable=False)
    created_at = Column(String(64), nullable=False)
    id = Column(String(60), nullable=False, primary_key=True)

    def __init__(self, token, user_id):
        super().__init__()
        self.id = token
        self.user_id = user_id
    
    @classmethod
    def user_by_session(cls, session):
        session = cls.get_by_id(session)
        if not session:
            return None
        return session.user_id
    
    @classmethod
    def sessions_by_user(cls, user_id):
        sessions = cls.get_where('user_id', user_id)
        if not sessions:
            return None
        return sessions
 