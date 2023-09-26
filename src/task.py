import datetime
import string

class Task:
    id: int
    title: string
    detail: string
    deadline: datetime
    priority: int

    def __init__(self, 
                 taskId: int, 
                 title: string, 
                 detail: string = None, 
                 deadline: datetime = None, 
                 priority: int = 1) -> None:
        self.id = taskId
        self.title = title
        self.detail = detail
        self.deadline = deadline
        self.priority = priority

    def __eq__(self, other) -> bool:
        if isinstance(other, Task):
            return (self.id == other.id and 
                    self.title == other.title and 
                    self.detail == other.detail and 
                    self.deadline == other.deadline and 
                    self.priority == other.priority)
        
        return False