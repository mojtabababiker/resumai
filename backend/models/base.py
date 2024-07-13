#!/usr/bin/env python3
""" A module that holds the database base model abstarction
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4, UUID
from models import dbEngine

@dataclass
class Base:
    """The base database models abstraction
    """
    # id: UUID = field(default_factory=uuid4)
    # created_at: datetime = field(default_factory=datetime.now)
    # updated_at: datetime = field(default_factory=datetime.now)


    def __getattribute__(self, name: str) -> Any:
        """get the attribute of the model, to handle UUID or Datetime convertion to string
        """
        if name == 'id':
            return str(self._id)
        if name in ['created_at', 'updated_at'] and isinstance(self.__dict__.get(name, None), datetime):
            return self.__dict__[name].strftime('%Y-%m-%dT%H:%M:%S')
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """set the attribute of the model, to handle string convertion to UUID or Datetime
        """
        if name == 'id' and isinstance(value, str):
            self._id = UUID(value)
        if name in ['created_at', 'updated_at'] and isinstance(value, str):
            self.__dict__[name] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        super().__setattr__(name, value)

    async def save(self) -> str | None:
        """Save the model object to the database

        Returns:
        --------
        * str: the id of the saved document or None if the save failed
        """
        collection = f"{self.__class__.__name__.lower()}s"
        model_doc = self.to_dict()
        result = await dbEngine.save(collection, model_doc)
        return result

    async def delete(self) -> bool:
        """Delete the model from the database

        Returns:
        --------
        * bool: True if the delete operation was successful, False otherwise
        """
        collection = f"{self.__class__.__name__.lower()}s"
        result = await dbEngine.delete(collection, self.id)
        return result

    async def update(self, data: dict) -> bool:
        """Update the model in the database by setting the data

        Parameters:
        -----------
        * data: dict: the data to update the model with

        Returns:
        --------
        * bool: True if the update operation was successful, False otherwise
        """
        collection = f"{self.__class__.__name__.lower()}s"
        filtered_data = {k: v for k, v in data.items()
                         if k not in ['id', 'created_at']}
        result = await dbEngine.update(collection, self.id, filtered_data)
        return result
    
    async def update_resumes(self, op: str, resume: object) -> bool:
        """Update the user's resumes in the database

        Parameters:
        -----------
        * op: str: the operation to perform on the resumes list
        * resume: Resume object: the resume object to push/delete into/from the user's resumes

        Returns:
        --------
        * bool: True if the update operation was successful, False otherwise
        """
        collection = f"{self.__class__.__name__.lower()}s"
        try:
            if op == 'push':
                return await dbEngine.db[collection].update_one(
                    {'_id': self.id},
                    {'$push': {'resumes': resume.to_dict()}}  # type: ignore
                )
            elif op == 'pop':
                return await dbEngine.db[collection].update_one(
                    {'_id': self.id},
                    {'$pull': {'resumes': {'_id': resume.id}}}  # type: ignore
                )
        except Exception as e:
            # print(e)
            return False
        return False
    
    async def edit_resume(self, resume_id:str, updates:dict):
        """Update the user resume with the id resume_id by setting the fields in the update_data
        
        Parameters:
        -----------
        
        * resume_id: str: the id of the resume to update
        * update_data: dict: dictionary contains the data fields to update
        
        """
        collection = f"{self.__class__.__name__.lower()}s"
        update_objects = {"$set": {}}  # the update object to be passed to the update_one method

        update_data = updates.pop('data', None)  # if the updates contains the resume data field
        if update_data:
            update_objects["$set"].update(
                # then for each field in the data field, update the field in the database
                {f"resumes.$.data.{key}": val for key, val in update_data.items()}
            )

        # add the rest of the fields to the update object if they are allowed to be updated 
        update_objects["$set"].update(
            {f"resumes.$.{key}": val for key, val in updates.items() if key in ['updated_at', 'templateId']}
        )
        # print(update_objects)
        try:
            result = await dbEngine.db[collection].update_one(
                {"_id": self.id, "resumes._id": resume_id},
                update=update_objects,
            )
        except Exception as e:
            # print(e)
            return False
        return result.modified_count > 0

    @classmethod
    async def find_one(cls, query: dict) -> object | None:
        """Find one document in the database

        Parameters:
        -----------
        * query: dict: the query to search for

        Returns:
        --------
        * Any: the document found or None if not found
        """
        collection = f"{cls.__name__.lower()}s"
        result = await dbEngine.find_one(collection, query)
        if result:
            return cls.from_dict(result)  # type: ignore
        return None
