#!/usr/bin/env python3
"""Holds all the schemas used in the user operations and endpoints"""
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """The user creation schema"""
    first_name: str
    last_name: str
    email: EmailStr
    password: str  # type: ignore
