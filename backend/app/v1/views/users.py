#!/usr/bin/env python3
"""User views module for the API."""
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

# import schemas
from app.v1.schema.user_schemas import UserCreate, UserOut
from app.v1.schema.auth_schemas import Token

# import dependencies
from app.v1.utils.access_token import create_access_token, get_current_user

# User database model
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        201: {"description": "Created successfully"},
        200: {"description": "Success"},
        401: {"description": "Unauthorized"},
        400: {"description": "Bad Request"},
        }
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[UserCreate, Body()]) -> Token:
    """Create and register a new user, and return an access token
    
    Parameters:
    -----------
    * **user**: UserCreate: the user data to create the user with
    
    Returns: Token: the `access token`
    """
    if await User.find_one({"email":user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user = User(**user.model_dump())
    await new_user.save()
    access_token = await create_access_token(new_user.id)
    return Token(access_token=access_token, token_type="bearer")

@router.get('/me')
async def get_me(user: User = Depends(get_current_user)) -> UserOut:
    """Get the current user's data
    
    Parameters:
    -----------
    * **user**: User: the current user
    
    Returns: UserOut: the current user's data
    """
    user_profile = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "is_active": user.is_active
    }
    return UserOut(**user_profile)
