# Project defines the interface for adding data

from dataclasses import dataclass
from typing import Callable
from gsorter.group import Grouper, Group
from pydantic import BaseModel, Field

class Project(BaseModel):
    name : str = ''
    groups : list[Group] = Field(default_factory=lambda:[])
    userdata : dict = Field(default_factory=lambda: {})

    def load_from_path(file_path):
        with open(file_path, encoding='utf-8') as f:
            self.model_validate_json(f.read())