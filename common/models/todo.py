from dataclasses import dataclass
from rococo.models import VersionedModel

@dataclass
class Todo(VersionedModel):
    person_id: str = ""
    title: str = ""
    completed: bool = False