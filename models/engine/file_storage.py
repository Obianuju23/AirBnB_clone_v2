#!/usr/bin/python3
"""Importing some Standard modules and modules from our packages"""
import json
from datetime import datetime as dt
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

"""
This is a Python class that will be responsible for file storage. In this
class, objects will be serialized into a JSON string object and saved to a
flat database (json file)
"""


class FileStorage():
    """
    This is a class responsible for data storage for AirBnB Clone project.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self) -> dict:
        """
        This is a public instance method that returns the private instance
        attribute `__object` which is a dictionary

        Return:
              A dictionary of objects
        """
        return FileStorage.__objects

    def new(self, obj: dict) -> None:
        """
        This is a public instance method that adds a new object to the
        dictionary of objects (`__objects`)

        Args:
            obj (dict) - a dictionaary object
        """
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[obj_key] = obj

    def save(self) -> None:
        """
        This is a public instance method that serializes the private instance
        attribute `__objects` (dict) into a JSON string and save it to a flat
        database (json file)
        """
        dict_serial = {}
        with open(self.__file_path, mode="w", encoding="utf-8") as file_obj:
            for key, val in self.__objects.items():
                dict_serial[key] = val.to_dict()
            json.dump(dict_serial, file_obj)

    def reload(self) -> None:
        """
        This is a public instance method that deserializes a json string into
        a dictionary of object, `__objects` only if `__file_path` exist.
        """
        try:
            path = self.__file_path
            with open(path, mode="r", encoding="utf-8") as file_obj:
                data_strm = json.load(file_obj)
            for key, val in data_strm.items():
                class_name = key.split(".")[0]
                self.new(eval(class_name + "(**val)"))
        except FileNotFoundError:
            pass
