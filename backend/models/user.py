#!/usr/bin/env python3
""" A module that holds the database model abstarction for the resumes document
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID
from bcrypt import hashpw, checkpw, gensalt
from models.base import Base
from models.resume import Resume


@dataclass
class User(Base):
    """The user database model abstraction
    """
    first_name: str
    last_name: str
    email: str
    password: str  # type: ignore
    _id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    profile_img: Optional[str] = None
    resumes: List[Resume] = field(default_factory=list)  # TODO: forbid setting resumes from outside the class
    is_active: bool = False
    is_admin: bool = False

    @property
    def full_name(self):
        """Return the full name of the user
        """
        return f"{self.first_name} {self.last_name}"
    
    @property
    def password(self):
        """Return the password of the user
        """
        # return self._hased_password
        raise AttributeError("User class has no attribute password")
    
    @password.setter
    def password(self, password: str):
        """Set the password of the user
        """
        try:
            if len(password) < 24:
                self._hashed_password = hashpw(password.encode(), gensalt(12)).decode("utf-8")
            else:
                self._hashed_password = password
        except Exception:
            # raise ValueError("The password could not be hashed, or already hashed")
            self._hashed_password = password  # security risk, TODO: seek a better way to handle this

    def check_password(self, password: str) -> bool:
        """ validate the user enterded password
        
        Parameters:
        -----------
        * password: str: the password to validate

        Returns:
        ----------
        * bool: True if the password is correct, False otherwise
        """
        return checkpw(password.encode(), self._hashed_password.encode())


    def to_dict(self):
        """Convert the object instance to a dictionary ready to be save on database

        Returns:
        --------
        dict: the dictionary representation of the object instance containing
        """
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self._hashed_password,
            "profile_img": self.profile_img,
            "resumes": [resume.to_dict() for resume in self.resumes],
            "is_active": self.is_active,
            "is_admin": self.is_admin
        }
    
    @classmethod
    def from_dict(cls, user_dict: dict):
        """Convert a dictionary to a User object instance
        
        Parameters:
        -----------
        * user_dict: dict: a dictionary containing the user data
        
        Returns:
        --------
        User: a User object instance
        """
        user = cls(
            first_name=user_dict["first_name"],
            last_name=user_dict["last_name"],
            email=user_dict["email"],
            password=user_dict["password"],
            _id=user_dict["_id"],
            created_at=user_dict["created_at"],
            updated_at=user_dict["updated_at"],
            profile_img=user_dict["profile_img"],
            is_active=user_dict["is_active"],
            is_admin=user_dict["is_admin"]
        )
        for resume in user_dict["resumes"]:
            user.resumes.append(Resume.from_dict(resume))
        return user

    async def add_resume(self, resume: Resume):
        """Add a resume to the user's resumes
        """ 
        self.resumes.append(resume)
        return await self.update_resumes(op='push', resume=resume)

    async def remove_resume(self, resume_id: str):
        """Remove a resume from the user's resumes
        """
        # resume = [resume for resume in self.resumes if resume.id == resume_id] or None
        # if resume:
        try:
            resume = [resume for resume in self.resumes if resume.id == resume_id][0]
            self.resumes.remove(resume)
            return await self.update_resumes(op='pop', resume=resume)
        except (ValueError, IndexError):
            raise ValueError("The resume does not exist in the user's resumes")
