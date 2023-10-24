from dataclasses import dataclass
import xmlFileManager
from datetime import datetime
import string

TASK_TAG = "<task>"
TASK_END_TAG = "</task>" 
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

def XMLToTask(xml: string) -> Task:
    try:
        id = int(xml[xml.index("<id>") + 4:xml.index("</id>")])
        title = xml[xml.index("<title>") + 7:xml.index("</title>")]
        detail = xml[xml.index("<detail>") + 8:xml.index("</detail>")]
        deadline = xml[xml.index("<deadline>") + 10:xml.index("</deadline>")]
        priority = int(xml[xml.index("<priority>") + 10:xml.index("</priority>")])

        if not deadline.isspace():
            deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
        else:
            deadline = None
    
    except Exception as e:
        print(e)
        return
    
    return Task(id, title, detail, deadline, priority)

def saveTask(task: Task, savePath: string) -> bool :
    try:
        xmlFileManager.createXML(savePath, TASK_LIST_TAG)
        
        read_data: string = xmlFileManager.readFullXML(savePath)
                
        if not TASK_LIST_TAG or not TASK_LIST_END_TAG in read_data:
            raise OSError("ERROR: Not a Task Stack file")
        
        if "<id>{task.id}</id>" in read_data:
            xmlFileManager.updateXMLElement(taskToXML(task))
        xmlFileManager.appendXMLElement(taskToXML(task), savePath, TASK_LIST_TAG)

    except ValueError:
        print(f"ERROR: File '{savePath}' cannot be opened due to an encoding error.")
        return False
    
    except Exception as e:
        print(e)
        return False

    return True

def getTaskById(id: int) -> Task:
    

def getTasksFromXML(xmlList: string, taskList: list[Task]) -> list[Task]:
    if(TASK_TAG not in xmlList):
        return taskList

    newTaskXML = xmlList[xmlList.index(TASK_TAG):xmlList.index(TASK_END_TAG) + len(TASK_END_TAG)]
    newList = xmlList.replace(newTaskXML, "")
    newTask = XMLToTask(newTaskXML)

    if not newTask == None:
        taskList.append(newTask)

    return getTasksFromXML(newList, taskList)

def getTaskList(savePath: string) -> list[Task]:
    taskList: list[Task] = list()
    read_data: string = xmlFileManager.readFullXML(savePath)

    if not TASK_LIST_TAG or not TASK_LIST_END_TAG in read_data:
            raise OSError("ERROR: Not a Task Stack file")
    
    return getTasksFromXML(read_data, taskList)

if __name__ == "__main__":
    tacheBidon = Task(1, "tâche bidon", "", datetime.today())
    if(saveTask(tacheBidon, "test1/test2/test.xml")):
        print(getTaskList("test1/test2/test.xml"))
    else:
        print(":(")