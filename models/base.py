from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy import Column, String
from datetime import datetime


declarative_base = declarative_base()

class Base():
    id = Column(String(60), nullable=False, primary_key=True)
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        for k, v in kwargs.items():
            if k == "created_at":
                self.__dict__[k] = datetime.strptime(v, date_format)
            if k != "__class__":
                self.__dict__[k] = v
        
        
    
    def save(self):
        from models.storage import DB
        DB.save(self)
    
    def delete(self):
        from models.storage import DB
        DB.delete(self)
    
    @classmethod
    def get_by_id(cls, id):
        from models.storage import DB
        return DB.get_by_id(cls, id)
    
    @classmethod
    def get_by_handle(cls, handle):
        from models.storage import DB
        return DB.get_by_handle(cls, handle)
    
    @classmethod
    def get_all(cls):
        from models.storage import DB
        return DB.get_all(cls)
    
    @classmethod
    def get_where(cls, attribute, value):
        from models.storage import DB
        objects = cls.get_all()
        matches = []
        for object in objects:
            if object.__dict__[attribute] == value:
                matches.append(object)
        return matches

    @classmethod
    def get_all_list_of_dicts(cls):
        objects = cls.get_all()
        if not objects:
            return None
        dict_reprs = []
        for object in objects:
            del object._sa_instance_state
            dict_reprs.append(object.to_dict())
        return dict_reprs
    
    def to_dict(self):
        dict_repr = self.__dict__
        if 'password' in dict_repr:
            del dict_repr['password']
        return self.__dict__



