from gsorter.group import Folder
# Project defines the interface for adding data

# add_data(filesystem_path) returns a List of Folder
# Folder.files() returns a List of File
# File.fields() returns a List of Field

from dataclasses import dataclass
from typing import Callable
from group import Folder

# Should this be a dataclass?
@dataclass
class ProjectSpec:
    add_data: Callable[list[str],Group]

class Project:
    def __init__(self, spec):
        self.spec = spec
        self._groups = []
        self.active_group = None

    def add_data(self, file_paths : list[str]):
        self._groups.append(spec.add_data(file_paths))
