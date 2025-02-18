#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the get method"""
        new_state = State(name="California")
        new_state.save()
        retrieved_state = models.storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)
        self.assertIsInstance(retrieved_state, State)
        models.storage.delete(new_state)  # Cleanup

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_none(self):
        """Test get method with invalid ID"""
        self.assertIsNone(models.storage.get(State, "invalid_id"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count method"""
        initial_count = models.storage.count()
        new_user = User(email="test@example.com", password="password123")
        new_user.save()
        self.assertEqual(models.storage.count(), initial_count + 1)
        models.storage.delete(new_user)  # Cleanup

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_class(self):
        """Test the count method with a class"""
        initial_state_count = models.storage.count(State)
        new_state = State(name="New York")
        new_state.save()
        self.assertEqual(models.storage.count(State), initial_state_count + 1)
        models.storage.delete(new_state)  # Cleanup


if __name__ == "__main__":
    unittest.main()
