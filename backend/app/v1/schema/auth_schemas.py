#!/usr/bin/env python3
"""Holds all the schemas used in the authentication process"""
from pydantic import BaseModel

class TokenData(BaseModel):
    """The token data schema"""
    id: str
    scoop: str
