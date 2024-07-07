"""An abstarct class for mongo database engine"""
from dataclasses import dataclass, field
from os import environ
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DBEngine:
    """MongoDB engine class, responsible for handling all database operations"""
    def __init__(self):
        """Initialize the database engine, and construct the client and database objects
        """
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(environ.get('HOST', 'localhost'), int(environ.get('PORT', 27017)))
        self.db: AsyncIOMotorDatabase = self.client[environ.get("DB_NAME", 'test_db')]  # type: ignore
    
    async def save(self, collection: str, data: dict) -> str | None:
        """Save data to the database

        Parameters:
        -----------

        * collection: str: the collection to save the data in
        * data: dict: the dictionary representation of the data to save
        """
        try:
            await self.db[collection].insert_one(data)
        except Exception as e:
            print(e)
            return None
        return str(data['_id'])
    
    async def delete(self, collection: str, _id: str) -> bool:
        """Delete data from the database

        Parameters:
        -----------

        * collection: str: the collection to delete the data from
        * _id: str: the id of the data to delete
        """
        try:
            await self.db[collection].delete_one({"_id": _id})
        except Exception as e:
            print(e)
            return False
        return True

    async def update(self, collection: str, _id: str, data: dict) -> bool:
        """Update data in the database

        Parameters:
        -----------

        * collection: str: the collection to update the data in
        * _id: str: the id of the data to update
        * data: dict: the dictionary representation of the data to update
        """
        try:
            result = await self.db[collection].update_one({"_id": _id}, {"$set": data})
        except Exception as e:
            print(e)
            return False
        return result.modified_count > 0
    
    async def find_one(self, collection: str, query: dict) -> dict | None:
        """Find one document in the database

        Parameters:
        -----------

        * collection: str: the collection to search on
        * query: dict: the query to search for
        """
        try:
            return await self.db[collection].find_one(query)
        except Exception as e:
            print(e)
            return None



async def main():
    """Test the DBEngine class
    """
    db = DBEngine()

    # Test save
    data = {
        "_id": "123",
        "firstName": "janet",
        "lastName": "Doe",
        "email": "jadoe@foo.bar",
        "password": "password1",
        "is_active": True,
        "is_admin": False,
        "created_at": "2021-10-10",
        "updated_at": "2021-10-10",
        "profile_img": "profile.jpg",
        "resumes": [{
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
                },
        }]
    }
    print("Saving data")
    resutl = await db.save("users", data)
    print(resutl)
    data['resumes'].append({
        '_id': 'f2611d97-2a4a-4df0-abbe-39bc5d074baa',
        'created_at': '2024-01-01T00:00:00',
        'updated_at': '2024-01-01T00:00:00',
        'templateId': 'f2611d97-2a4a-4afc-abbe-39bc5d074b6e',
        'data': {
            'title': {
                'name': 'Jane Doe',
                'jobTitle': 'Software Engineer',
                'links': [
                    {
                        'type': 'linkedIn',
                        'linkUrl': 'https://www.linkedin.com/in/janedoe'
                    },
                    {
                        'type': 'GitHub',
                        'linkUrl': 'https://www.github.com/in/janedoe',
                    },
                ],
            },
            'summary': 'A software engineer with 5 years of experience in software development',
            'experiences': [
                {
                    'companyName': 'Google',
                    'roleTitle': 'Software Engineer',
                    'startingDate': '2016-01-01',
                    'endingDate': '2021-01-01',
                    'location': 'Mountain View, CA',
                    'summary': 'Worked on the search engine team'
                }
            ],
            'education': [
                {
                    'schoolName': 'MIT',
                    'degreeTitle': 'Bachelor of Science in Computer Science',
                    'startingDate': '2012-01-01',
                    'endingDate': '2016-12-31',
                    'location': 'Cambridge, MA',
                    'summary': 'Graduated with honors'
                }
            ],
            'skills': ['Python', 'JavaScript', 'React', 'C++'],
            'languages': [
                {
                    'name': 'English',
                    'proficient': 'native'
                },
                {
                    'name': 'Spanish',
                    'proficient': 'proficient'
                }
            ],
        }
    })
    print("Updating data")
    await db.update("users", "123", data)
    print()
    print("Finding data")
    result = await db.find_one("users", {"_id": "123"})
    print(result)
    print()
    print("Deleting data")
    await db.delete("users", "123")
    print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
