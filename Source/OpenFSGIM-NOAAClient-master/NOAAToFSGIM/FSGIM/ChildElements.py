import xml.etree.ElementTree as ET
from FSGIM import Link

class ChildElements(object):

    @staticmethod
    def createXMLTags(root, elements, list):
        lenList = len(list)
        for x in range(0, lenList):
            ET.SubElement(root, list[x]).text = elements[list[x]]

        return root

    @staticmethod
    def createChildGeneric(root, elements):
        for value in elements:
            ET.SubElement(root, value[0]).text = str(value[1])

        return root

