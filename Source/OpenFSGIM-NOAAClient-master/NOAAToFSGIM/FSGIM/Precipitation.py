import uuid
import xml.etree.ElementTree as ET
from FSGIM import UUIDFSGIM, ChildElements, UTCTime, Link, BaseElement
import time, datetime


class Precipitation:

    def __init__(self,precipitationValue, validT, description, parent, lowerCoordinates, upperCoordinates):
        self.Entry = ET.Element("entry")
        self.lowerC = lowerCoordinates
        self.upperC = upperCoordinates
        self.parent = parent
        self.updateTime = UTCTime.UTCTime.getTime()
        self.description = description
        self.validTComponents = validT.split("/")
        self.atomResource = 'fsgimprecipitation'
        name = description + '/' + self.atomResource + '/' + self.updateTime + '/' + validT
        self.mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, name)

        #-------------------------------------------------------------------
        #
        #  Since Dictionaries are randomly sequenced, we need to provide a list of the proper
        #  sequence for XML Entries to be generated to ensure compliance with the FSGIM Weather schema
        #
        #-------------------------------------------------------------------

        self.listAtomElement = []
        self.listAtomElement.append('id')
        self.listAtomElement.append('title')
        self.listAtomElement.append('published')
        self.listAtomElement.append('updated')

        self.entryAtomElement = {
            'id': self.mRID,
            'title': 'FSGIM Precipitation',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': 'FSGIMPrecipitation',
            'nameType': 'Forecast',
        }

        # self.contentElements = {
        #     'description': description,
        #     'duration' : validTComponents[1],
        # }

        self.listAbstractMeasure = []
        self.listAbstractMeasure.append('value')
        self.listAbstractMeasure.append('uom')

        self.depthElements = {
            'value': str(precipitationValue),
            'uom':'m',
        }

    def getAtomEntry(self):
        ChildElements.ChildElements.createXMLTags(self.Entry, self.entryAtomElement, self.listAtomElement)
        links = set([('self', self.description),
                     ('up', self.parent)
                     ])
        Link.Link.createLinks(self.Entry, links)
        content = ET.SubElement(self.Entry,"content")
        type = ET.SubElement(content, "FSGIMPrecipitation")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        BaseElement.BaseElement.addBoundedBy(type, self.lowerC, self.upperC)
        ET.SubElement(type, "description").text = self.description
        depthElement = ET.SubElement(type, "depth")
        ChildElements.ChildElements.createXMLTags(depthElement, self.depthElements, self.listAbstractMeasure)
        # Precipitation.generateAbstractMovement(self,content)
        # Precipitation.generateAbstractMovement(self,content)
        # Precipitation.generateAbstractMovement(self,content)
        ET.SubElement(type, "duration").text = self.validTComponents[1]
        return self.Entry
