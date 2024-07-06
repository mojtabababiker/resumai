#!/usr/bin/env python3
""" A module that holds the database base model abstarction
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4, UUID

@dataclass
class Base:
    """The base database models abstraction
    """
    # id: UUID = field(default_factory=uuid4)
    # created_at: datetime = field(default_factory=datetime.now)
    # updated_at: datetime = field(default_factory=datetime.now)


    def __getattribute__(self, name: str) -> Any:
        """get the attribute of the model, to handle UUID or Datetime convertion to string
        """
        if name == 'id':
            return str(self._id)
        if name in ['created_at', 'updated_at'] and isinstance(self.__dict__.get(name, None), datetime):
            return self.__dict__[name].strftime('%Y-%m-%dT%H:%M:%S')
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """set the attribute of the model, to handle string convertion to UUID or Datetime
        """
        if name == 'id' and isinstance(value, str):
            self._id = UUID(value)
        if name in ['created_at', 'updated_at'] and isinstance(value, str):
            self.__dict__[name] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        super().__setattr__(name, value)

    def save(self):
        """Save the model to the database
        """
        pass

    def delete(self):
        """Delete the model from the database
        """
        pass

    def update(self):
        """Update the model in the database
        """
        pass