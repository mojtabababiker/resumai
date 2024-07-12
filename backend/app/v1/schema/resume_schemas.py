#!/usr/bin/env python3
"""Holds all the schemas used in the user's resumes operations and endpoints"""
from datetime import datetime
from pydantic import BaseModel
from dataclasses import dataclass, field
from enum import Enum


class LinkType(Enum):
    """The link type enum class that represent the type of the link
    
    Options:
    --------
    * LINKEDIN
    * GITHUB
    """
    LINKEDIN = "linkedIn"
    GITHUB = "GitHub"


class LanguageProficiencyLevel(Enum):
    """The language proficiency level enum class that represent the proficiency level of a language
    
    Options:
    --------
    * BEGINNER
    * INTERMEDIATE
    * GOOD_WORKING_KNOWLEDGE
    * PROFICIENT
    * NATIVE
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    GOOD_WORKING_KNOWLEDGE = "good working knowledge"
    PROFICIENT = "proficient"
    NATIVE = "native"


# @dataclass
class Link(BaseModel):
    """The link dataclass that represent the link field in the resume
    
    Parameters:
    -----------
    * type: LinkType, the type of the link [linkedIn, GitHub]
    * linkUrl: str, the url of the link
    """
    type: str
    linkUrl: str


# @dataclass
class Title(BaseModel):
    """The title dataclass that represent the title field in the resume
    
    Parameters:
    -----------
    * name: str, the name of the person
    * jobTitle: str, the job title appling for
    * links: List[Link], the list of links to the person's social media
    """
    name: str
    jobTitle: str
    links: list[Link] | None = field(default_factory=list)


# @dataclass
class Experience(BaseModel):
    """The experience dataclass that represent the experience field in the resume

    Parameters:
    -----------
    * companyName: str, the name of the company
    * roleTitle: str, the title of the role in the company
    * startingDate: datetime, the starting date of the job
    * endingDate: Optional[datetime], the ending date of the job
    * location: str, the location of the company
    * summary: str, the summary of the experience
    """
    companyName: str
    roleTitle: str
    location: str
    summary: str
    startingDate: str
    endingDate: str|None = None


# @dataclass
class Project(BaseModel):
    """The Project dataclass that represent the project field in the resume

    Parameters:
    -----------
    * title: str, the title of the project
    * description: str, the description of the project
    """
    title: str
    description: str


# @dataclass
class Education(BaseModel):
    """The education dataclass that represent the education field in the resume

    Parameters:
    -----------
    * schoolName: str, the name of the school
    * degreeTitle: str, the title of the degree
    * startingDate: Optional[datetime], the starting date of the education
    * endingDate: Optional[datetime], the ending date of the education
    * location: str, the location of the school
    * summary: str, Optional summary of the education
    """
    schoolName: str
    degreeTitle: str
    location: str
    summary: str|None = None
    startingDate: str|None = None
    endingDate: str|None = None

   
# @dataclass
class Achievement(BaseModel):
    """The achievement dataclass that represent the achievement field in the resume

    Parameters:
    -----------
    * title: str, the title of the achievement
    * description: str, the description of the achievement
    """
    title: str
    description: str


# @dataclass
class Certificate(BaseModel):
    """The certificate dataclass that represent the certificate field in the resume

    Parameters:
    -----------
    * title: str, the title of the certificate
    * description: str, the description of the certificate
    """
    title: str
    description: str


# @dataclass
class Language(BaseModel):
    """The language dataclass that represent the language field in the resume

    Parameters:
    -----------
    * name: str, the name of the language
    * proficient: LanguageProficiencyLevel, the proficiency level of the language
    """
    name: str
    proficient: LanguageProficiencyLevel

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
    templateId: str | None = None
    updated_at: str | None = None
    data: ResumeData | None = None
