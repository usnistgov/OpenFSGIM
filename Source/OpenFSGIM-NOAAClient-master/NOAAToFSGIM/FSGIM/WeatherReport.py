import uuid
import xml.etree.ElementTree as ET
from FSGIM import UUIDFSGIM, ChildElements,UTCTime, Link, BaseElement
import time, datetime


class WeatherReport:

    def __init__(self, description, lowerCoordinate, upperCoordinate, updateT, validT):
        #initializing class variables
        self.Entry = ET.Element("entry")
        self.upperC = upperCoordinate
        self.lowerC = lowerCoordinate

        self.updateTime = UTCTime.UTCTime.getTime()
        self.atomResource = 'fsgimweatherreport'
        name = description + '/' + self.atomResource + '/' + updateT + '/' + validT
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
            'title': 'FSGIM Weather Report',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': 'FSGIMWeatherReport',
            'nameType': 'Report',
        }

        self.listContentElements = []
        self.listContentElements.append('description')
        self.listContentElements.append('automated')
        self.listContentElements.append('issueTime')
        self.listContentElements.append('missing')
        self.listContentElements.append('raw_text')

        self.contentElements = {
            'description': description,
            'automated':'false',
            'issueTime': self.updateTime,
            'missing':'false',
            'raw_text':'Ut nisi orci, consequat a metus ut, aliquet fermentum lectus. In pretium vehicula aliquam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur rdiculus mus',
        }

    def getEntryElement(self):
        ChildElements.ChildElements.createXMLTags(self.Entry, self.entryAtomElement, self.listAtomElement)
        #include code to add atom links into the entry element
        links = set([('self', 'https://www.usnist.gov/fsgim/1_0/source/Weather/Report/'),
                     ])
        Link.Link.createLinks(self.Entry, links)

        content = ET.SubElement(self.Entry, "content")
        type = ET.SubElement(content, "FSGIMWeatherReport")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        BaseElement.BaseElement.addBoundedBy(type, self.lowerC, self.upperC)
        ChildElements.ChildElements.createXMLTags(type, self.contentElements, self.listContentElements)

        return self.Entry




