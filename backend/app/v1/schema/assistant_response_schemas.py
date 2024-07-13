#!/usr/bin/env python3
"""Holds all the schemas used in the Ai assistant operations and endpoints"""
from pydantic import BaseModel

from app.v1.schema.resume_schemas import ResumeData


class ScoringInsight(BaseModel):
    """The scoring insight dataclass that represent the scoring insights of the resume
    
    * score: float, the score of the resume
    * insights: list[str], the assistant insights and tips"""
    score: float
    insights: list[str]

class EnhanceOut(BaseModel):
    """The enhance out dataclass that represent the enhanced resume data and scoring insights
    
    Parameters:
    -----------
    * resume_data: dict, the enhanced resume data
    * scoring_insights: dict, the scoring insights of the resume
    """
    resume_data: ResumeData
    scoring_insights: ScoringInsight

