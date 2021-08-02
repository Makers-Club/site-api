from os import getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base import declarative_base



class MySQLClient():
    def __init__(self, credentials):
        # ISOLATION LEVEL READ UNCOMMITTED FORCES THE CLIENT TO MAKE FRESH QUERIES INTO THE DB EACH TIME
        self.__engine = create_engine(URL.create(**credentials), isolation_level="READ UNCOMMITTED", pool_pre_ping=True)
    
    def reload(self):
        declarative_base.metadata.create_all(self.__engine)
        sf = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session()

    def is_connected(self):
        return True if self.__engine else False
    
    def save(self, obj):
        self.__session.add(obj)
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            try:
                self.__session.commit()
            except Exception:
                self.__session.rollback()
                self.__session.commit()
            
    
    def delete(self, obj):
        self.__session.delete(obj)
        try:
            self.__session.commit()
        except:
            self.__session.rollback()

    def get_all(self, cls):
        try:
            return self.__session.query(cls).all()
            
        except:
            self.__session.rollback()
            return None
        
    
    def get_by_id(self, cls: type, id: str):
        result = self.__session.query(cls).filter_by(id=str(id))
        if not result:
            return None
        try:
            return result.first()
        except Exception:
            self.__session.rollback()
            return None


    def get_by_handle(self, cls: type, handle: str):
        result = self.__session.query(cls).filter_by(handle=handle)
        if not result:
            return None
        try:
            return result.first()
        except Exception:
            self.__session.rollback()
            return None
    