#!/usr/bin/python3
"""
class DBStorage
"""


import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "State": State, "Amenity": Amenity,
           "Place": Place, "Review": Review, "City", City}


class DBStorage:
    """MySQL database"""
    __session = None
    __engine = None

    def __init__(self):
        """DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on current database session"""
        new_dic = {}
        for cl in classes:
            if cls is None or cls is classes[cl] or cls is cl:
                objs = self.__session.query(classes[cl]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dic[key] = obj
        return (new_dic)

    def new(self, obj):
        """current database session"""
        self.__session.add(obj)

    def save(self):
        """changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """drop from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """retrieve object"""
        if cls and id:
            object = models.storage.all(cls)
            for i, j in object.items():
                if j.id == id:
                    return j
        return None

    def count(self, cls=None):
        """count the number of objects in storage"""
        return len(models.storage.all(cls))
