import os
import string

ENCODING = "utf-8"
XMLHEADERS = "<?xml versions=\"1.0\" encoding=\"" + ENCODING + "\"?>"

def writeXMLFile(xmlString: string, filePath: string):
    with open(filePath, "w", encoding=ENCODING) as f:
        f.write(xmlString)

def createXML(filePath: string, newTag: string = None) -> bool :
    directory = "/".join(filePath.split("/")[:-1])

    if not os.path.exists(directory):
        os.makedirs(directory)
            
    if not os.path.exists(filePath):
        headers = XMLHEADERS + "\n"
        if(newTag and not newTag.isspace()):
            headers += newTag + "\n" + newTag[:1] + "/" + newTag[1:]
        writeXMLFile(headers, filePath)

    if os.path.exists(filePath):
        return True
    return False

def getXMLElement(filePath: string, openTag: string, identifier: string = None) -> string:
    with open(filePath, "r", encoding=ENCODING) as f:
        read_data = f.read()
    closeTag: string = openTag[:1] + "/" + openTag[1:]

    if not identifier or  identifier.isspace():
        index = read_data.index(openTag)
        closeIndex = read_data.index(closeTag) + len(closeTag)
        return read_data[index:closeIndex]      


    index = read_data.index(identifier)
    reversedData = read_data[index::-1]
    reversedTag = reversed(openTag)
    distance = reversedData.index(reversedTag)
    index -= distance #index of <openTag>
    closeIndex = read_data.index(closeTag, index) + len(closeTag)
    return read_data[index:closeIndex]
    
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

def updateXMLElement(newXML: string, oldXML: string, savePath: string) -> bool:
    xmlDocument: string = readFullXML(savePath)
    updatedDocument = xmlDocument.replace(oldXML, newXML, 1)
    if newXML not in updatedDocument:
        return False
    writeXMLFile(updatedDocument, savePath)
    return True