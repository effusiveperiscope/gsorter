from row import Row
@dataclass
class Group:
    name: str
    groups: list[Group]
    rows: list[Row]
