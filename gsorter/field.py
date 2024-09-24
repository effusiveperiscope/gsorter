from pydantic import BaseModel, Field
from PyQt5.QtGui import (QIntValidator, QDoubleValidator)

class FieldSpec(BaseModel):
    field_type: str
    optional: bool = False
    editable: bool = True
    flags: dict = Field(default_factory=lambda:{})