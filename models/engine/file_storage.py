#!/usr/bin/python3
"""
FileStorage class
"""

import json
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"User": User, "BaseModel": BaseModel, "Amenity": Amenity,
           "Place": Place, "Review": Review, "State": State, "City": City}


class FileStorage:
    """serializes & deserializes to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns dictionary __objects"""
        if cls is not None:
            new_dt = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dt[key] = value
            return new_dt
        return self.__objects

    def new(self, obj):
        """sets __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to (path: __file_path)"""
        json_obj = {}
        for key in self.__objects:
            json_obj[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                j_obj = json.load(f)
            for key in j_obj:
                self.__objects[key] = classes[j_obj[key]["__class__"]](**j_obj[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """reload() method for deserializing the JSON file to objects"""
        self.reload()

    def count(self, cls=None):
        """count the number of objects in storage"""
        return len(models.storage.all(cls))

    def get(self, cls, id):
        """A method to retrieve an object"""
        if cls and id:
            object = models.storage.all(cls)
            for i, j in object.items():
                if j.id == id:
                    return j
        return None
