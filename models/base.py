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
            if k != "__class__":
                # tried this to get rid of error: 'list' object has no attribute '_sa_adapter'
                # did not work
                # setattr(self, str(k), str(v))
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
        queries = [DB.get_all(cls) for x in range(10)]
        for q in queries:
            if q:
                return q
        raise Exception(DB)
    
    @classmethod
    def get_where(cls, attribute, value):
        from models.storage import DB
        objects = cls.get_all()
        matches = []
        for object in objects:
            obj_attr = object.__dict__[attribute]
            if isinstance(obj_attr, str):
                obj_attr = obj_attr.lower()
            # next line ensures it's comparing them as the same type
            if obj_attr == type(obj_attr)(value):
                matches.append(object)
        return matches

    @classmethod
    def get_all_list_of_dicts(cls):
        objects = cls.get_all()
        if not objects:
            return None
        all_obj_dicts = []
        for obj in objects:
            obj_dict = {}
            for k, v in obj.__dict__.items():
                if hasattr(v, 'id'):
                    obj_dict[k] = v.id
                    continue
                if isinstance(v, list):
                    obj_dict[k] = [x.id for x in v]
                    continue
                if k != '_sa_instance_state':
                    obj_dict[k] = v
            all_obj_dicts.append(obj_dict)
        return all_obj_dicts
    
    def to_dict(self):
        dict_repr = self.__dict__
        if 'password' in dict_repr:
            del dict_repr['password']
        return self.__dict__



