import os
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from utils.db_engine import DBEngine


class TestDBEngine(IsolatedAsyncioTestCase):
    """Test the DBEngine class
    """
    @classmethod
    def setUpClass(cls):
        """Set up the test class
        """
        cls.db_host = os.getenv('DB_HOST', 'localhost')
        cls.db_port = int(os.getenv('DB_PORT', 27017))
        cls.test_client = MongoClient(host=cls.db_host, port=cls.db_port)
        cls.test_db = cls.test_client['test_db']

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class
        """
        cls.test_client.close()

    def tearDown(self):
        """Clean the database after each test
        """
        self.test_db.drop_collection('test')

    def test_init(self):
        """Test the __init__ method
        """
        dbEngine = DBEngine()
        self.assertIsNotNone(dbEngine)
        self.assertIsInstance(dbEngine.client, AsyncIOMotorClient)
        self.assertIsInstance(dbEngine.db, AsyncIOMotorDatabase)
        self.assertEqual(dbEngine.db.name, 'test_db')
        self.assertEqual(dbEngine.client.HOST, self.db_host)
        self.assertEqual(dbEngine.client.PORT, self.db_port)
        dbEngine.client.close()

    async def test_save(self):
        """Test the save method, normal case
        """
        dbEngine = DBEngine()
        data = {"_id": "1", "name": "test"}
        id = await dbEngine.save("test", data)
        db_result = self.test_db['test'].find_one({"_id": id})
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result['name'], "test")  # type: ignore
        dbEngine.client.close()

    async def test_save_exception(self):
        """Test the save method, exception case
        """
        dbEngine = DBEngine()
        dbEngine.db = MagicMock()
        dbEngine.db.__getitem__.side_effect = Exception()
        data = {"_id": "2", "name": "test"}
        id = await dbEngine.save("test", data)
        self.assertIsNone(id)
        db_result = self.test_db['test'].find_one({"_id": "2"})
        self.assertIsNone(db_result)
        dbEngine.client.close()

    async def test_delete(self):
        """Test the delete method, normal case
        """
        dbEngine = DBEngine()
        data = {"_id": "3", "name": "test"}
        self.test_db['test'].insert_one(data)
        result = await dbEngine.delete("test", "3")
        self.assertTrue(result)
        db_result = self.test_db['test'].find_one({"_id": "3"})
        self.assertIsNone(db_result)
        dbEngine.client.close()

    async def test_delete_exception(self):
        """Test the delete method, exception case
        """
        dbEngine = DBEngine()
        dbEngine.db = MagicMock()
        dbEngine.db.__getitem__.side_effect = Exception()
        result = await dbEngine.delete("test", "4")
        self.assertFalse(result)
        dbEngine.client.close()

    async def test_update(self):
        """Test the update method, normal case
        """
        self.test_db['test'].insert_one({"_id": "5", "name": "test"})
        dbEngine = DBEngine()
        data = {"name": "updated"}
        result = await dbEngine.update("test", "5", data)
        self.assertTrue(result)
        db_result = self.test_db['test'].find_one({"_id": "5"})
        self.assertEqual(db_result['name'], "updated")  # type: ignore
        dbEngine.client.close()

    async def test_update_exception(self):
        """Test the update method, exception case
        """
        dbEngine = DBEngine()
        dbEngine.db = MagicMock()
        dbEngine.db.__getitem__.side_effect = Exception()
        data = {"name": "updated"}
        result = await dbEngine.update("test", "6", data)
        self.assertFalse(result)
        dbEngine.client.close()

    async def test_find_one(self):
        """Test the find_one method, normal case
        """
        self.test_db['test'].insert_one({"_id": "7", "name": "test"})
        dbEngine = DBEngine()
        query = {"_id": "7"}
        result = await dbEngine.find_one("test", query)
        self.assertEqual(result['name'], "test")  # type: ignore
        dbEngine.client.close()

    async def test_find_one_exception(self):
        """Test the find_one method, exception case
        """
        dbEngine = DBEngine()
        dbEngine.db = MagicMock()
        dbEngine.db.__getitem__.side_effect = Exception()
        query = {"_id": "8"}
        result = await dbEngine.find_one("test", query)
        self.assertIsNone(result)
        dbEngine.client.close()

    async def test_find_one_not_found(self):
        """Test the find_one method, not found case
        """
        dbEngine = DBEngine()
        query = {"_id": "9"}
        result = await dbEngine.find_one("test", query)
        self.assertIsNone(result)
        dbEngine.client.close()
