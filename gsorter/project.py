# Project defines the interface for adding data

from dataclasses import dataclass
from typing import Callable
from gsorter.group import Grouper, Group
from pydantic import BaseModel, Field

class Project(BaseModel):
    name : str = ''
    groups : list[Group] = Field(default_factory=lambda:[])
    userdata : dict = Field(default_factory=lambda: {})