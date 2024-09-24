from gsorter.item import Item
from pydantic import BaseModel, Field
class Comparison(BaseModel):
    comparison_id: str = ''
    data: list[Item] = Field(default_factory=lambda:[])
    selected_item: int = 0