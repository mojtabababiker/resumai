#!/usr/bin/env python3
"""Users Resumes views model"""
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

@router.get('/{resume_id}')
async def get_resume(resume_id: str, user: Annotated[User, Depends(get_current_user)]) -> Resume:
    """Get the user Resume with id equal to resume_id, and returns it
    
    Parameters:
    -----------
    * **resume_id**: str: the id of the required Resume
    * **user**: User: the current logged in user object
    
    Returns: Resume: the object contains all the `resume fields`
    """
    try:
        resume = [resume_object for resume_object in user.resumes if resume_object.id == resume_id][0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return resume

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_resume(
    resume: Annotated[ResumeCreate, Body()],
    user: Annotated[User, Depends(get_current_user)]
    ) -> str:
    """Create a new Resume for the logged in user, and return its ID
    
    Parameters:
    -----------
    * **resume**: Resume: the data to create a resume with
    
    Returns: str: the created resume `id`
    """
    resume_dict = resume.model_dump()
    templateId = resume_dict.pop('templateId')
    resume_object = Resume(templateId=templateId, data=Resume._data_from_dict(resume_dict))
    if not await user.add_resume(resume_object):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An Error occurred please try again later'
        )
    return resume_object.id

@router.delete('/')
async def delete_resume(
    resume_id: str, 
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Create a new Resume for the logged in user, and return its ID
    
    Parameters:
    -----------
    * **resume_id**: str: the resume id to be deleted
    """
    exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume Not found"
        )
    try:
        deleted = await current_user.remove_resume(resume_id=resume_id)
    except ValueError:
        raise exception
    if not deleted:
        raise exception
