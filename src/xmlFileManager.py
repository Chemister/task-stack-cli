import os
import string

ENCODING = "utf-8"
XMLHEADERS = "<?xml versions=\"1.0\" encoding=\"" + ENCODING + "\"?>"


def createXML(filePath: string, newTag: string = None) -> bool :
    directory = "/".join(filePath.split("/")[:-1])

    if not os.path.exists(directory):
        os.makedirs(directory)
            
    if not os.path.exists(filePath):
        with open(filePath, "w", encoding=ENCODING) as f:
            headers = XMLHEADERS + "\n"

            if(newTag and not newTag.isspace()):
                headers += newTag + "\n" + newTag[:1] + "/" + newTag[1:] 

            f.write(headers)

    if os.path.exists(filePath):
        return True
    return False


def readFullXML(filePath: string) -> string :
    read_data: string 
    with open(filePath, "r", encoding=ENCODING) as f:
        read_data = f.read()

    if not XMLHEADERS in read_data:
        raise OSError("ERROR: Not an XML file or incorrect XML header")
    
    return read_data


def appendXMLElement(xmlString: string, filePath: string, xmlElementTag: string):
    if not xmlElementTag and not xmlElementTag.isspace():
        raise ValueError("ERROR: Element Tag cannot be empty")
    
    endTag = xmlElementTag[:1] + "/" + xmlElementTag[1:] 
    read_data = readFullXML(filePath)

    if not xmlElementTag in read_data:
        read_data += "\n" + xmlElementTag + "\n" + endTag 
    
    offset = read_data.index(endTag)

    with open(filePath, "w", encoding=ENCODING) as f:  
        f.write(read_data[:offset] + xmlString + endTag)