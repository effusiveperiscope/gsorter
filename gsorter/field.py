from typing import Union, Callable
from dataclasses import dataclass
from PyQt5.QtGui import (QIntValidator, QDoubleValidator)

@dataclass
class FieldSpec:
    name: str,
    field_type: type,
    validator: Union[
        QIntValidator,
        QDoubleValidator, 
        Callable[..., bool]]

@dataclass
class FieldFill:
    name: str,
    values: list
