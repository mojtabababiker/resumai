import unittest
from datetime import datetime
from models.user import User
from models.resume import Resume
from uuid import UUID

class TestUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.resume_dict = {
            "_id": "f2611d97-2a4a-4df0-abbe-39bc5d074b6e",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "templateId": "f2611d97-2a4a-4afc-abbe-39bc5d074b6e",
            "data": {
                "title": {
                    "name": "John Doe",
                    "jobTitle": "Software Engineer",
                    "links": [
                        {
                            "type": "linkedIn",
                            "linkUrl": "https://www.linkedin.com/in/johndoe"
                        },
                        {
                            "type": "GitHub",
                            "linkUrl": "https://www.github.com/in/johndoe",
                        },
                    ],
                },
                "summary": "A software engineer with 5 years of experience in software development",
                "experiences": [
                    {
                        "companyName": "Google",
                        "roleTitle": "Software Engineer",
                        "startingDate": "2016-01-01",
                        "endingDate": "2021-01-01",
                        "location": "Mountain View, CA",
                        "summary": "Worked on the search engine team"
                    }
                ],
                "education": [
                    {
                        "schoolName": "MIT",
                        "degreeTitle": "Bachelor of Science in Computer Science",
                        "startingDate": "2012-01-01",
                        "endingDate": "2016-12-31",
                        "location": "Cambridge, MA",
                        "summary": "Graduated with honors"
                    }
                ],
                "skills": ["Python", "JavaScript", "React"],
                "languages": [
                    {
                        "name": "English",
                        "proficient": "native"
                    },
                    {
                        "name": "Spanish",
                        "proficient": "proficient"
                    }
                ],
            }
        }
        self.resume = Resume.from_dict(self.resume_dict)
        self.user = User(first_name="John", last_name="Doe", email="john@doe.com", password="1234", is_active=True, is_admin=True)

    def test_full_name(self):
        self.assertEqual(self.user.full_name, "John Doe")

    def test_password(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_set_password(self):
        self.user.password = "new_password"
        self.assertTrue(self.user.check_password("new_password"))

    def test_check_password(self):
        self.assertTrue(self.user.check_password("1234"))
        self.assertFalse(self.user.check_password("wrong_password"))

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict["_id"], self.user.id)
        self.assertEqual(user_dict["created_at"], self.user.created_at)
        self.assertEqual(user_dict["updated_at"], self.user.updated_at)
        self.assertEqual(user_dict["first_name"], self.user.first_name)
        self.assertEqual(user_dict["last_name"], self.user.last_name)
        self.assertEqual(user_dict["email"], self.user.email)
        self.assertEqual(user_dict["password"], self.user._hashed_password)
        self.assertEqual(user_dict["profile_img"], self.user.profile_img)
        self.assertEqual(user_dict["resumes"], [resume.to_dict() for resume in self.user.resumes])
        self.assertEqual(user_dict["is_active"], self.user.is_active)
        self.assertEqual(user_dict["is_admin"], self.user.is_admin)

    def test_from_dict(self):
        user_dict = self.user.to_dict()
        user2 = User.from_dict(user_dict)
        self.assertIsInstance(user2, User)
        self.assertEqual(user2.first_name, self.user.first_name)
        self.assertEqual(user2.last_name, self.user.last_name)
        self.assertEqual(user2.email, self.user.email)
        self.assertEqual(user2._hashed_password, self.user._hashed_password)
        self.assertEqual(user2.profile_img, self.user.profile_img)
        self.assertEqual(user2.resumes, self.user.resumes)
        self.assertEqual(user2.is_active, self.user.is_active)
        self.assertEqual(user2.is_admin, self.user.is_admin)

    async def test_add_resume(self):
        await self.user.add_resume(self.resume)
        self.assertIn(self.resume, self.user.resumes)

    async def test_remove_resume(self):
        await self.user.add_resume(self.resume)
        await self.user.remove_resume(self.resume.id)
        self.assertNotIn(self.resume, self.user.resumes)

if __name__ == "__main__":
    unittest.main()