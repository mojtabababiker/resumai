#!/usr/bin/env python3
"""Users Resumes views model"""
from os import wait
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

# import schemas
from app.v1.schema.auth_schemas import Token
from app.v1.schema.resume_schemas import ResumeCreate

# import dependencies
from app.v1.utils.access_token import get_current_user

# import database models
from models.user import User
from models.resume import Resume

router = APIRouter(
    prefix='/resumes',
    tags=['resume']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_resume(
    resume: Annotated[ResumeCreate, Body()],
    user: Annotated[User, Depends(get_current_user)]
    ) -> dict:
    """Create a new Resume for the logged in user, and return its ID
    
    Parameters:
    -----------
    * **resume**: Resume: the data to create a resume with
    
    Returns: str: the created resume `id`
    """
    resume_dict = resume.model_dump(exclude_unset=True)
    templateId = resume_dict.pop('templateId')
    resume_object = Resume(templateId=templateId, data=Resume._data_from_dict(resume_dict))
    if not await user.add_resume(resume_object):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An Error occurred please try again later'
        )
    # await user.save()
    return resume_object.to_dict()

