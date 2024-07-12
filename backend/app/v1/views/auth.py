#!/usr/bin/env python3
"""The views module for the authentication endpoints
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.v1.schema.auth_schemas import Token
from app.v1.utils.access_token import create_access_token, get_current_user

# User database model
from models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/session", response_model=str)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login the user based on the provided credentials and return an access token
    
    Parameters:
    -----------
    * **form_data**: OAuth2PasswordRequestForm: the form data containing the user credentials (username and password)
    
    Returns: str: the `access token`
    """
    email = form_data.username
    password = form_data.password
    remember_me = form_data.scopes[0]
    user: User| None = await User.find_one({"email": email})  # type: ignore
    if not user or not user.check_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    duration = 0 if remember_me == 'checked' else 1440 # 1 day
    token = await create_access_token(user.id, duration)
    return Token(access_token=token, token_type="bearer")
    