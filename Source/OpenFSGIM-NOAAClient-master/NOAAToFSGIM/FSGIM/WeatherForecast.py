import uuid
import xml.etree.ElementTree as ET
from . import UUIDFSGIM, ChildElements, UTCTime, Link
from dateutil import parser


class WeatherForecast:

    def __init__(self, validT, description, updateT, atomLinks):
        self.Entry = ET.Element("entry")
        self.updateT = updateT
        self.validT = validT
        self.validTime = validT.split("/")
        self.updateTime = UTCTime.UTCTime.getTime()
        self.atomResource = 'fsgimweatherforecast'
        name = description + '/' + self.atomResource + '/' + self.updateT + '/' + self.validT
        self.mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, name)
        self.atomLinks = atomLinks

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
            'title': 'FSGIM Weather Forecast',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': 'FSGIMWeatherForecast',
            'nameType': 'Forecast',
        }

        self.listContentElements = []
        self.listContentElements.append('resultQuality')
        self.listContentElements.append('resultTime')
        self.listContentElements.append('samplingTime')
        #self.listContentElements.append('confidence')
        #self.listContentElements.append('forecastAnalysisTime')

        self.contentElements = {
            'resultQuality': '',
            'resultTime': updateT,
            'samplingTime': updateT,
            #'confidence': '',
            # 'confidenceRange': '',
            #'forecastAnalysisTime': updateT,
        }

    def getAtomEntry(self):
        ChildElements.ChildElements.createXMLTags(self.Entry, self.entryAtomElement, self.listAtomElement)
        Link.Link.createLinks(self.Entry,self.atomLinks)
        content = ET.SubElement(self.Entry,"content")
        type = ET.SubElement(content, "FSGIMWeatherForecast")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        ChildElements.ChildElements.createXMLTags(type, self.contentElements, self.listContentElements)
        confidence = ET.SubElement(type, "confidence")
        ET.SubElement(confidence, "maxInclusive").text = "0"
        ET.SubElement(confidence, "minInclusive").text = "0"
        ET.SubElement(type, 'forecastAnalysisTime').text = self.updateT
        probability = ET.SubElement(type, "probability")
        ET.SubElement(probability, "maxInclusive").text = "100"
        ET.SubElement(probability, "minInclusive").text = "100"
        #ET.SubElement(type, "validTime").text = self.validTime
        valid_time_xml = ET.SubElement(type, "validTime")
        if len(self.validTime) == 2:
            ET.SubElement(valid_time_xml, 'duration').text = self.validTime[1]
            ET.SubElement(valid_time_xml, 'start').text = parser.parse(self.validTime[0]).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        elif len(self.validTime) == 1:
            ET.SubElement(valid_time_xml, 'start').text = parser.parse(self.validTime[0]).strftime(
                "%Y-%m-%dT%H:%M:%SZ")

        return self.Entry
