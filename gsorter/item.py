from pydantic import BaseModel, Field
class Item(BaseModel):
    comparison_id: str = ''
    data: dict = Field(default_factory=lambda: {})
    editable: bool = True
    selected: bool = True
    modification_timestamps: dict = Field(default_factory=lambda: {})