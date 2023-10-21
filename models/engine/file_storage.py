#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            if type(cls) == str:
                return {k: v for k, v in self.__objects.items()
                        if v.__class__.__name__ == cls}
            else:
                return {k: v for k, v in self.__objects.items()
                        if v.__class__ == cls}
        else:
            return self.__objects

    def delete(self, obj=None):
        """"
        to delete obj from __objects if it’s inside - if obj is equal to None
        """
        if obj is not None:
            del self.__objects[obj.__class__.__name__ + '.' + obj.id]
            self.save()

    def new(self, obj):
        """Adds new object to storage dictionary"""
        k = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[k] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            json_obj = {key: value.to_dict() for key,
                    value in self.__objects.items()}
            json.dump(json_obj, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                    }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                jl = json.load(f)
                for k in jl:
                    self.__objects[k] = classes[jl[k]["__class__"]](**jl[k])
        except:
            pass
