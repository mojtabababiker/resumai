#!/usr/bin/env python3
""" A module that holds the database model abstraction for the resumes document
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID

from pydantic_core import Url

from models.base import Base


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


class Link(BaseModel):
    """The link dataclass that represent the link field in the resume
    
    Parameters:
    -----------
    * type: str, the type of the link [linkedIn, GitHub]
    * linkUrl: str, the url of the link
    """
    type: str
    linkUrl: str


class Title(BaseModel):
    """The title dataclass that represent the title field in the resume
    
    Parameters:
    -----------
    * name: str, the name of the person
    * jobTitle: str, the job title applying for
    * links: List[Link], the list of links to the person's social media
    """
    name: str
    jobTitle: str
    links: list[Link] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'Title':
        """Convert the dictionary to a title object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the title
        
        Returns:
        --------
        Title: the title object instance
        """
        return cls(
            name=data['name'],
            jobTitle=data['jobTitle'],
            links=[Link(type=item['type'], linkUrl=item['linkUrl']) for item in data['links']]
        )


class Project(BaseModel):
    """The Project dataclass that represent the project field in the resume

    Parameters:
    -----------
    * title: str, the title of the project
    * description: str, the description of the project
    """
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Convert the dictionary to a project object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the project
        
        Returns:
        --------
        Project: the project object instance
        """
        return cls(
            title=data['title'],
            description=data['description']
        )


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
    startingDate: datetime|None|str = None
    endingDate: datetime|None|str = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Education':
        """Convert the dictionary to an education object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the education
        
        Returns:
        --------
        Education: the education object instance
        """
        return cls(
            schoolName=data['schoolName'],
            degreeTitle=data['degreeTitle'],
            location=data['location'],
            summary=data['summary'] if 'summary' in data else None,
            startingDate=data['startingDate'],
            endingDate=data['endingDate'] if 'endingDate' in data else None
        )


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
    summary: Optional[str]
    startingDate: datetime
    endingDate: datetime|str = 'present'

    @classmethod
    def from_dict(cls, data: dict) -> 'Experience':
        """Convert the dictionary to an experience object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the experience
        
        Returns:
        --------
        Experience: the experience object instance
        """
        # if data['endingDate'] is None:
        #     endingDate = None
        # elif data['endingDate'] == 'present':
        #     endingDate = 'present'
        # else:
        #     endingDate = datetime.strptime(data['endingDate'], "%Y-%m-%d")
        return cls(
            companyName=data['companyName'],
            roleTitle=data['roleTitle'],
            startingDate=data['startingDate'], # datetime.strptime(data['startingDate'], "%Y-%m-%d"),
            endingDate=data['endingDate'], # endingDate,  # type: ignore
            location=data['location'],
            summary=data['summary'] if data['summary'] else None
        )

   
class Achievement(BaseModel):
    """The achievement dataclass that represent the achievement field in the resume

    Parameters:
    -----------
    * title: str, the title of the achievement
    * description: str, the description of the achievement
    """
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Achievement':
        """Convert the dictionary to an achievement object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the achievement
        
        Returns:
        --------
        Achievement: the achievement object instance
        """
        return cls(
            title=data['title'],
            description=data['description']
        )


class Certificate(BaseModel):
    """The certificate dataclass that represent the certificate field in the resume

    Parameters:
    -----------
    * title: str, the title of the certificate
    * description: str, the description of the certificate
    """
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Certificate':
        """Convert the dictionary to a certificate object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the certificate
        
        Returns:
        --------
        Certificate: the certificate object instance
        """
        return cls(
            title=data['title'],
            description=data['description']
        )


class Language(BaseModel):
    """The language dataclass that represent the language field in the resume

    Parameters:
    -----------
    * name: str, the name of the language
    * proficient: LanguageProficiencyLevel, the proficiency level of the language
    """
    name: str
    proficient: str  # LanguageProficiencyLevel

    @classmethod
    def from_dict(cls, data: dict) -> 'Language':
        """Convert the dictionary to a language object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the language
        
        Returns:
        --------
        Language: the language object instance
        """
        return cls(
            name=data['name'],
            proficient=data['proficient']
        )


@dataclass
class ResumeData:
    """The data that represent the resume containing the information
    about each field in the resume.

    Parameters:
    -----------
    * title: Title, the title field that contain name, job title, and optional links
    * summary: str, the summary or the objectives 
    * experiences: List[Experience], the list of experiences
    * education: List[Education], the list of education
    * achievements: List[Achievement], the list of achievements
    * certificates: List[Certificate], the list of certificates
    * skills: List[str], the list of skills
    * languages: List[Language], the list of languages
    """
    title: Title
    summary: str
    projects: list[Project] = field(default_factory=list)
    experiences: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    achievements: list[Achievement]|None = field(default_factory=list)
    certificates: list[Certificate]|None = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    languages: list[Language] = field(default_factory=list)


@dataclass
class Resume(Base):
    """The resume dataclass that represent the resume document in the database containing all the fields
    
    Parameters:
    -----------
    
    * data: ResumeData, the data that represent the resume containing the information about each field in the resume
    * id: UUID, the unique identifier of the resume saved as an index in the database
    * created_at: datetime, the date and time the resume was created
    * updated_at: datetime, the date and time the resume was last updated
    * templateId: str, the template (html file) id of the resume
    """
    data: ResumeData = field(default_factory=ResumeData)  # type: ignore
    _id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    templateId: str = field(default_factory=str)

    def to_dict(self) -> dict:
        """Convert the object instance to a dictionary ready to be save on database

        Returns:
        --------
        dict: the dictionary representation of the object instance containing the fields of the resume
        """
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "templateId": str(self.templateId),
            "data": self._data_to_dict(self.data)
        }

    def _data_to_dict(self, obj):
        """A recursive function that convert the resume data to a dictionary
        
        Parameters:
        -----------
        
        * obj: any, the object to be converted to a dictionary, at start it's the resume data: ResumeData
        
        Returns:
        --------
        dict: the dictionary representation of the resume data
        """
        if isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, (UUID, Url)):
            return str(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, list):
            return [self._data_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._data_to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, '__dict__'):
            return {k: self._data_to_dict(v) for k, v in obj.__dict__.items()}
        # else:
        #     return str(obj)

    @classmethod
    def from_dict(cls, data: dict) -> 'Resume':
        """Convert the dictionary to a resume object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the resume
        
        Returns:
        --------
        Resume: the resume object instance
        """
        return cls(
            data=cls._data_from_dict(data['data']),
            _id=data['_id'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            templateId=data['templateId']

        )
    
    @classmethod
    def _data_from_dict(cls, data: dict) -> 'ResumeData':
        """Convert the dictionary to a resume data object instance
        
        Parameters:
        -----------
        
        * data: dict, the dictionary representation of the resume data
        
        Returns:
        --------
        ResumeData: the resume data object instance
        """
        return ResumeData(
            title=Title.from_dict(data['title']),
            summary=data['summary'],
            projects=[Project.from_dict(item) for item in data['projects']],
            experiences=[Experience.from_dict(item) for item in data['experiences']],
            education=[Education.from_dict(item) for item in data['education']],
            achievements=[Achievement.from_dict(item) for item in data['achievements']] if data.get('achievements', None) else None,
            certificates=[Certificate.from_dict(item) for item in data['certificates']] if data.get("certificates", None) else None,
            skills=data['skills'],
            languages=[Language.from_dict(item) for item in data['languages']]
        )
