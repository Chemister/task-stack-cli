from dataclasses import dataclass
import datetime
import os
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
    
def taskToXML(task: Task) -> string:
    return f"""
<task>
    <id>{task.id}</id>
    <title>{task.title}</title>
    <detail>{task.detail or ''}</detail>
    <deadline>{task.deadline or ''}</deadline>
    <priority>{task.priority}</priority>
<task/>"""

def saveTask(task: Task, savePath: string) -> bool :
    data: string = ""

    try:
        if not os.path.exists(savePath):
            f = open(savePath, "w")
            f.close()

        with open(savePath, "r+", encoding="utf-8") as f:
            read_data = f.read()
            if not "<?xml versions=\"1.0\" encoding=\"utf-8\"?>" in read_data:
                data = "<?xml versions=\"1.0\" encoding=\"utf-8\"?>"
            
            data += taskToXML(task)
            
            if (len(data) > 0):
                f.write(data)

    except ValueError:
        print(f"ERROR: File '{savePath}' cannot be opened due to an encoding error.")
        return False
    
    except Exception as e:
        print(e)
        return False

    return True

if __name__ == "__main__":
    tacheBidon = Task(1, "tâche bidon")
    if(saveTask(tacheBidon, "test.xml")):
        print("Succès!")
    else:
        print(":(")