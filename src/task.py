from dataclasses import dataclass
import datetime
import string

@dataclass
class Task:
    id: int
    title: string
    detail: string = None
    deadline: datetime = None
    priority: int = 1

    def __eq__(self, other) -> bool:
        if isinstance(other, Task):
            return (self.id == other.id and 
                    self.title == other.title and 
                    self.detail == other.detail and 
                    self.deadline == other.deadline and 
                    self.priority == other.priority)
        
        return False