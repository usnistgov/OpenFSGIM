import uuid
import xml.etree.ElementTree as ET
from FSGIM import UUIDFSGIM, ChildElements, BaseElement, Link, UTCTime
import time, datetime


class WeatherArea:

    def __init__(self, description, lowerCoordinate, upperCoordinate, parent, updateT, validT):
        self.Entry = ET.Element("entry")
        self.description = description
        self.upperC = upperCoordinate
        self.lowerC = lowerCoordinate
        self.parent = parent
        self.updateT = updateT
        self.validT = validT

        self.updateTime = UTCTime.UTCTime.getTime()
        self.atomResource = 'fsgimweatherarea'
        name = description + '/' + self.atomResource + '/' + self.updateT + '/' + self.validT
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
            'title': 'FSGIM Weather Area',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': 'FSGIMWeatherArea',
            'nameType': 'Area',
        }

    def getAtomEntry(self):
        ChildElements.ChildElements.createXMLTags (self.Entry, self.entryAtomElement, self.listAtomElement)
        links = set([('self', self.description+'/' + self.atomResource),
                     ('up', self.parent)
                     ])
        Link.Link.createLinks(self.Entry, links)
        content = ET.SubElement(self.Entry, "content")
        type = ET.SubElement(content, "FSGIMWeatherArea")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        BaseElement.BaseElement.addBoundedBy(type,self.lowerC, self.upperC)
        ET.SubElement(type, "description").text = self.description
        return self.Entry