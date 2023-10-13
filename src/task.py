from dataclasses import dataclass
import xmlFileManager
import datetime
import os
import string

TASK_LIST_TAG = "<tasks>"
TASK_LIST_END_TAG = "</tasks>"
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


def taskToXML(task: Task) -> string:
    return f"""<task>
    <id>{task.id}</id>
    <title>{task.title}</title>
    <detail>{task.detail or ''}</detail>
    <deadline>{task.deadline or ''}</deadline>
    <priority>{task.priority}</priority>
</task>
"""


def saveTask(task: Task, savePath: string) -> bool :
    try:
        xmlFileManager.createXML(savePath, TASK_LIST_TAG)
        
        read_data: string = xmlFileManager.readFullXML(savePath)
                
        if not TASK_LIST_TAG or not TASK_LIST_END_TAG in read_data:
            raise OSError("ERROR: Not a Task Stack file")
        
        xmlFileManager.appendXMLElement(taskToXML(task), savePath, TASK_LIST_TAG)

    except ValueError:
        print(f"ERROR: File '{savePath}' cannot be opened due to an encoding error.")
        return False
    
    except Exception as e:
        print(e)
        return False

    return True


if __name__ == "__main__":
    tacheBidon = Task(1, "tâche bidon", "", datetime.datetime.today())
    if(saveTask(tacheBidon, "test1/test2/test.xml")):
        print("Succès!")
    else:
        print(":(")