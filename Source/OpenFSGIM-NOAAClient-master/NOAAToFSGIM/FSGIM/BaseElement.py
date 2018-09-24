import xml.etree.ElementTree as ET
from FSGIM import Link, ChildElements

class BaseElement():

    @staticmethod
    def getElement(name, id, title, links):
        rootElement = ET.Element(name)
        idChildElement = ET.SubElement(rootElement,"id")
        idChildElement.text = id
        ET.SubElement(rootElement,"title").text = title
        for link in links:
            linkChildElement = Link.Link.createLink(link[0], link[1])
            rootElement.append(linkChildElement)

        return  rootElement

    @staticmethod
    def addBoundedBy(root,lowerCoordinates, upperCoordinates):
        boundedBy = ET.SubElement(root, "boundedBy")
        lowerCorner = ET.SubElement(boundedBy, "lowerCorner")
        ChildElements.ChildElements.createChildGeneric(lowerCorner, lowerCoordinates)
        ET.SubElement(lowerCorner, "dimension").text = "2"
        upperCorner = ET.SubElement(boundedBy, "upperCorner")
        ChildElements.ChildElements.createChildGeneric(upperCorner, upperCoordinates)
        ET.SubElement(upperCorner, "dimension").text = "2"





