#!/usr/bin/env python3
"""Holds all the schemas used in the authentication process"""
from pydantic import BaseModel

class TokenData(BaseModel):
    """The jwt extracted token data schema"""
    id: str
    scoop: str

class Token(BaseModel):
    """The jwt token schema"""
    access_token: str
    token_type: str