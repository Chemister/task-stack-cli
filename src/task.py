from dataclasses import dataclass
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
        if not os.path.exists(savePath):
            f = open(savePath, "w", encoding="utf-8")
            headers = "<?xml versions=\"1.0\" encoding=\"utf-8\"?>\n" + TASK_LIST_TAG  + "\n" + TASK_LIST_END_TAG
            f.write(headers)
            f.close()
        
        read_data: string

        with open(savePath, "r", encoding="utf-8") as f:
            read_data = f.read()
            if not "<?xml versions=\"1.0\" encoding=\"utf-8\"?>" in read_data:
                raise OSError("ERROR: Not an XML file or incorrect XML header")
            
            if not TASK_LIST_TAG and TASK_LIST_END_TAG in read_data:
                raise OSError("ERROR: Not a Task Stack file")
        
        with open(savePath, "w", encoding="utf-8") as f:    
            offset = read_data.index(TASK_LIST_END_TAG)
            f.write(read_data[:offset] + taskToXML(task) + TASK_LIST_END_TAG)

    #except ValueError:
    #    print(f"ERROR: File '{savePath}' cannot be opened due to an encoding error.")
    #    return False
    
    except Exception as e:
        print(e)
        return False

    return True

if __name__ == "__main__":
    tacheBidon = Task(1, "tâche bidon", "", datetime.datetime.today())
    if(saveTask(tacheBidon, "test.xml")):
        print("Succès!")
    else:
        print(":(")