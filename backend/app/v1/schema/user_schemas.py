#!/usr/bin/env python3
"""Holds all the schemas used in the user operations and endpoints"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """The user base schema
    This schema is used to define the common fields for the user schema

    * first_name: str: the user's first name
    * last_name: str: the user's last name
    * email: EmailStr: the user's email address
    """
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    """The user creation schema
    This schema is used to define the fields required to create a user
    * first_name: str: the user's first name
    * last_name: str: the user's last name
    * email: EmailStr: the user's email address
    * password: str: the user's password
    """
    password: str

class UserOut(UserBase):
    """The user output schema
    This schema is used to define the fields to be returned in the response
    
    * id: str: the user's id
    * first_name: str: the user's first name
    * last_name: str: the user's last name
    * email: EmailStr: the user's email address
    * created_at: str: the user's creation date
    * updated_at: str: the user's last update date
    * is_active: bool: the user's active status
    """
    id: str
    created_at: str
    updated_at: str
    is_active: bool
