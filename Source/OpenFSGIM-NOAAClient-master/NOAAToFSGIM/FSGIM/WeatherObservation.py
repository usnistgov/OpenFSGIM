import uuid
import xml.etree.ElementTree as ET
from . import UUIDFSGIM, ChildElements, UTCTime, Link
from dateutil import parser
import datetime


class WeatherObservation:

    def __init__(self, description, atomLinks, updateT, validT):
        #initializing class variables
        self.Entry = ET.Element("entry")
        self.updateTime = updateT
        self.validTime = validT
        self.description = description
        self.atomResource = 'fsgimweatherobservation'
        name = description + '/' + self.atomResource + '/' + self.updateTime + '/' + self.validTime
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
            'title': 'FSGIM Weather Observation',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': 'FSGIMWeatherObservation',
            'nameType': 'Observation',
        }

        self.listContentElements = []
        self.listContentElements.append('resultQuality')
        self.listContentElements.append('resultTime')
        self.listContentElements.append('samplingTime')


        self.contentElements = {
            'resultQuality': '',
            'resultTime': self.updateTime,
            'samplingTime': self.updateTime,
        }

    def getAtomEntry(self):
        ChildElements.ChildElements.createXMLTags(self.Entry, self.entryAtomElement, self.listAtomElement)
        #include code to add atom links into the entry element
        links = set([(self, self.description),
                     ])
        Link.Link.createLinks(self.Entry, self.atomLinks)
        content = ET.SubElement(self.Entry, "content")
        type = ET.SubElement(content, "FSGIMWeatherObservation")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        ChildElements.ChildElements.createXMLTags(type, self.contentElements, self.listContentElements)
        valid_time_xml = ET.SubElement(type, "validTime")
        '''
         The NOAA weather API doesn't provide any duration for weather observation, validTime. 
         To add duration to validTime entry in FSGIM, This application uses the following step:
         
         -Round validTime.start up to the top of the hour and then,
          add one hour to that value to get validTime.end. 
         
         For example, let the start date be 2018-03-15T12:52:00Z rounded up to the next hour would be 
         2018-03-15T13:00:00Z then, adding one hour would make it 2018-03-15T14:00:00Z.
        
        2018-03-15T14:00:00Z will be the end date.
        '''

        endt = parser.parse(self.validTime)
        seconds = (endt.replace(tzinfo=None) - endt.min).seconds
        hr = 3600
        rounding = ((seconds+1800) // hr) * hr
        endDate = endt + datetime.timedelta(0, rounding - seconds, -endt.microsecond,0,0,1)

        ET.SubElement(valid_time_xml, 'end').text = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        ET.SubElement(valid_time_xml, 'start').text = parser.parse(self.validTime).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        return self.Entry

