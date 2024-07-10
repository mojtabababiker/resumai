import os
import unittest
import uuid
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from models import dbEngine

class TestUser(unittest.IsolatedAsyncioTestCase):
    """Integration test for the User model class"""

    @classmethod
    def setUpClass(cls):
        """Set up the database connection for all tests"""
        # cls.client = AsyncIOMotorClient(os.environ.get('HOST', 'localhost'), int(os.environ.get('PORT', 27017)))
        cls.testDB = dbEngine.db
        # Ensure the User model uses this database connection
        # User.set_db(cls.testDB)

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after all tests"""
        # cls.client.close()
        pass

    async def asyncSetUp(self):
        """Clear the database before each test"""
        await self.testDB.users.delete_many({})

    async def test_save(self):
        """Test save method of the user model class"""
        user_id = uuid.uuid4()
        user = User(
            _id=user_id,
            first_name="John",
            last_name="Doe",
            email="johndoe@foo.bar",
            password="password1",
            is_active=True,
            is_admin=False
        )
        try:
            id = await user.save()
            self.assertEqual(str(id), str(user_id))
            user_from_db = await self.testDB.users.find_one({"_id": str(user_id)})
            self.assertIsNotNone(user_from_db)
        except Exception as e:
            self.fail(f"test_save failed with error: {str(e)}")

    async def test_update(self):
        """Test update method of the user model class"""
        user_id = uuid.uuid4()
        user = User(
            _id=user_id,
            first_name="John",
            last_name="Doe",
            email="johndoe@foo.bar",
            password="password1",
            is_active=True,
            is_admin=False
        )
        try:
            await user.save()
            user.first_name = "Jane"
            await user.update({"first_name": "Jane"})
            user_from_db = await self.testDB.users.find_one({"_id": user_id})
            self.assertEqual(user_from_db["first_name"], "Jane")  # type: ignore
        except Exception as e:
            self.fail(f"test_update failed with error: {str(e)}")

if __name__ == "__main__":
    unittest.main()
