#!/usr/bin/env python3
"""Assistant views module for the API."""
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

# import assistant
from app.v1.schema.resume_schemas import ResumeData
from app.v1.utils.access_token import get_current_user
from app.v1.schema.assistant_response_schemas import EnhanceOut, ScoringInsight
from models.user import User
from utils import AIAssistant, jobCrawler  # type: ignore


router = APIRouter(
    prefix='/ai/enhance/resume',
    tags=['assistant'],
    dependencies=[Depends(get_current_user)]
)

@router.post('/')
async def enhance_resume(
    resume: Annotated[ResumeData, Body()],
    job_description: Annotated[str | None, Body()] = None,
    job_url: Annotated[str | None, Body()] = None,
    ) -> EnhanceOut:
    """Enhance the resume using teh AI assistance, either for specific job description or general enhancement
    The job description can be provided as a text or as a URL to a job post
    
    Parameters:
    * **resume**: ResumeData: the resume data to enhance
    * **job_description**: str | None: the job description to enhance the resume for, default to None
    * **job_url**: str | None: the URL to the job post, default to None
    
    Returns: EnhanceOut: the enhanced `resume data` and `scoring insights`
    """
    # resume_dict = resume.model_dump(exclude_defaults=True, exclude_none=True, exclude_unset=True)
    resume_dict = resume
    if job_description:
        enhanced_resume = await AIAssistant.enhance_resume(resume_dict, job_description.strip())
    elif job_url:
        job_description = jobCrawler.get_description(job_url)
        enhanced_resume = await AIAssistant.enhance_resume(resume_dict, job_description)
    else:
        enhanced_resume = await AIAssistant.enhance_resume(resume_dict)

    return EnhanceOut(
        resume_data=enhanced_resume['resume_data'],
        scoring_insights=ScoringInsight(
            score=enhanced_resume['scores']['acceptance_percentage'],
            insights=enhanced_resume['scores']['insights']
        )
    )
