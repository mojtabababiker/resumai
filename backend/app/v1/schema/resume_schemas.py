#!/usr/bin/env python3
"""Holds all the schemas used in the user's resumes operations and endpoints"""
from pydantic import BaseModel
from dataclasses import field
from enum import Enum


# import resume schemas from the resume models module
from models.resume import (
    Title,
    Experience,
    Project,
    Education,
    Achievement,
    Certificate,
    Language,

)


class ResumeData(BaseModel):
    """The Resume schema
    This schema is used to define the fields required to create a resume
    * title
    * summary
    * experiences: `Optional`
    * education
    * achievements: `optional`
    * certificates: `Optional`
    * skills
    * languages
    """
    title: Title | None = None
    summary: str | None = None
    education: list[Education] | None = None
    projects: list[Project] | None = None
    experiences: list[Experience] | None = None
    achievements: list[Achievement] | None = None
    certificates: list[Certificate] | None = None
    skills: list[str] | None = None
    languages: list[Language] | None = None


class ResumeCreate(BaseModel):
    """The Resume schema
    This schema is used to define the fields required to create a resume
    * templateId
    * title
    * summary
    * experiences: `Optional`
    * education
    * achievements: `optional`
    * certificates: `Optional`
    * skills
    * languages
    """
    templateId: str
    title: Title
    summary: str
    education: list[Education]
    projects: list[Project]
    experiences: list[Experience] = field(default_factory=list)
    achievements: list[Achievement] = field(default_factory=list)
    certificates: list[Certificate] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    languages: list[Language] = field(default_factory=list)


class ResumeUpdate(BaseModel):
    """The Resume schema
    This schema is used to define the fields required to create a resume
    * templateId: `Optional`
    * updated_at: `Optional`
    * title: `Optional`
    * summary:  `Optional`
    * experiences: `Optional`
    * education: `Optional`
    * achievements: `optional`
    * certificates: `Optional`
    * skills: `Optional`
    * languages: `Optional`
    """
    templateId: str | None = None
    updated_at: str | None = None
    data: ResumeData | None = None
