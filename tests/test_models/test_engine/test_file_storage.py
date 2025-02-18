#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import unittest

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        self.assertIsInstance(storage.all(), dict)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test the get method"""
        storage = FileStorage()
        new_state = State(name="California")
        new_state.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)
        self.assertIsInstance(retrieved_state, State)
        storage.delete(new_state)  # Cleanup

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_none(self):
        """Test get method with an invalid ID"""
        storage = FileStorage()
        self.assertIsNone(storage.get(State, "invalid_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test the count method"""
        storage = FileStorage()
        initial_count = storage.count()
        new_user = User(email="test@example.com", password="password123")
        new_user.save()
        self.assertEqual(storage.count(), initial_count + 1)
        storage.delete(new_user)  # Cleanup

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_class(self):
        """Test the count method with a specific class"""
        storage = FileStorage()
        initial_state_count = storage.count(State)
        new_state = State(name="New York")
        new_state.save()
        self.assertEqual(storage.count(State), initial_state_count + 1)
        storage.delete(new_state)  # Cleanup


if __name__ == "__main__":
    unittest.main()
