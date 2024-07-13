#!/usr/bin/env python3
"""Holds the utilities that handle the access token generation and
verification, and the user authentication"""
import asyncio  # for testing: DELETE ME
from datetime import datetime, timedelta, timezone, MAXYEAR
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt
# User database model
from models.user import User

# import schemas
from app.v1.schema.auth_schemas import TokenData


# The secret key used to sign the JWT token
__SECRET_KEY = "f54b6bc778e6cc12df51c9e5eb7a54d0eca3a2cf575737d20240db7c451a70eb"
# The algorithm used to sign the JWT token
__ALGORITHM = "HS256"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/session")

async def create_access_token(user_id: str, duration: int|None = None) -> str:
    """Create a new access token for the user, with the user_id as the payload
    
    Parameters:
    -----------
    * user_id: str: the id of the user to create the token for
    * duration: int|None: the expiration time of the token in seconds,
              if None the token will expire after 1 day (86400 seconds),
              if the value is less than 1 the token will not expire,
              defaults to None.
    
    Returns: str: the generated jwt token
    """
    if duration:
        expire_date = datetime.now(timezone.utc) + timedelta(minutes=duration, seconds=5.0)  # for specific purposes
    elif duration is not None and duration <= 0:
        expire_date = datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, timezone.utc) # never expire
    else:
        expire_date = datetime.now(timezone.utc) + timedelta(days=1)  # general uses
    
    payload = {"sub": f"User:{user_id}", "exp": expire_date}
    token = jwt.encode(payload, __SECRET_KEY, algorithm=__ALGORITHM)
    return token

async def verify_token(token: Annotated[str, Depends(oauth2_schema)]) -> TokenData:
    """ Verify if the token is valid token, and return the payload,
        if the token is invalid an exception will be raised with 401 status code

    Parameters:
    -----------
    * token: str: the token to verify

    Returns: TokenData: the token payload as TokenData
    """
    try:
        payload: dict = jwt.decode(token, __SECRET_KEY, algorithms=[__ALGORITHM])
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    sub:str = payload.get("sub")  # type: ignore
    scoop, id = sub.split(":")
    return TokenData(id=id, scoop=scoop)

async def get_current_user(token_data: Annotated[TokenData, Depends(verify_token)]) -> User:
    """Retrieve the user from database based on the access token data
    
    Parameters:
    -----------
    * token_data: TokenData: the token data used for retrieving user from database
    
    Returns: User: the user object
    """
    user: User|None = await User.find_one({"_id": token_data.id})  # type: ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")
    return user


if __name__ == "__main__":
    async def test():
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@doe.com",
            password="1234",
            is_active=True,
            is_admin=True
        )
        await user.save()
        
        token = await create_access_token(user.id, 1)
        print(token)
        token_data = await verify_token(token)
        print(f"\n{token_data}\n")
        retrieved_user = await get_current_user(token_data)
        print(f"{retrieved_user.full_name}")
    asyncio.run(test())
    