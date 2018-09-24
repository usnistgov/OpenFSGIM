import uuid
import xml.etree.ElementTree as ET
from . import UUIDFSGIM, ChildElements, UTCTime, Link, BaseElement
import datetime
from dateutil import parser

class WeatherBase:

    """Create a FSGIM Weather Base XML Entry

    Arguments:
      *self* -- file name or a file object opened for writing

      *pressure* -- the output encoding (default: US-ASCII)

      *air* -- bool indicating if an XML declaration should be
                           added to the output. If None, an XML declaration
                           is added if encoding IS NOT either of:
                           US-ASCII, UTF-8, or Unicode

      *dewPoint* -- sets the default XML namespace (for "xmlns")

      *maxTemp* -- either "xml" (default), "html, "text", or "c14n"

      *minTemp* -- controls the formatting of elements
                                that contain no content. If True (default)
                                they are emitted as a single self-closed
                                tag, otherwise they are emitted as a pair
                                of start/end tags

      *obsOrFcsTime* --

      *humidity* --

      *description* --

      *parent* --

      *lowerCoordinates* --

      *upperCoordinates* --

      *windDirection* --

      *windGust* --

      *windSpeed* --

    """

    #
    # -------------------------------------------------------------------

    def __init__(self, pressure, airTemp, dewPoint, maxTemp, minTemp, obsOrFcsTime, humidity, validT, description, parent, lowerCoordinates, upperCoordinates, windDirection, windGust, windSpeed, updateT):
        self.Entry = ET.Element("entry")
        self.pressure = pressure
        self.air = airTemp
        self.dewPoint = dewPoint
        self.max = maxTemp
        self.min = minTemp
        self.obsOrFcsTime = obsOrFcsTime
        self.humidity = humidity
        self.updateTime = UTCTime.UTCTime.getTime()
        self.validTime = validT.split("/")
        self.description = description
        self.parent = parent
        self.lowerC = lowerCoordinates
        self.upperC = upperCoordinates
        self.windDirection = windDirection
        self.wGust = windGust
        self.wSpeed = windSpeed

        self.name = 'FSGIMWeatherBase'
        self.atomResource = 'fsgimweatherbase'
        if description is not None and updateT is not None and validT is not None:
            name = description + '/' + self.atomResource + '/' + updateT + '/' + validT.replace("/", "%2F")
            self.mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, name)
        else:
            self.mRID = ''


        #-------------------------------------------------------------------
        #
        #  Since Dictionaries are randomly sequenced, we need to provide a list of the proper
        #  sequence for XML Entries to be generated to ensure compliance with the FSGIM Weather schema
        #
        #-------------------------------------------------------------------

    def add_data_readings(self, type):
        if self.pressure is not None:
            airPressure = ET.SubElement(type, "airPressure")
            ChildElements.ChildElements.createXMLTags(airPressure, self.airpressure, self.listAbstractMeasure)

        if self.air is not None:
            airTemp = ET.SubElement(type, "airTemperature")
            ChildElements.ChildElements.createXMLTags(airTemp, self.temperature, self.listAbstractMeasure)

        if self.dewPoint is not None:
            dewpoint = ET.SubElement(type, "dewpointTemperature")
            ChildElements.ChildElements.createXMLTags(dewpoint, self.dewpoint, self.listAbstractMeasure)

        if self.max is not None:
            maxTemp = ET.SubElement(type, "maxTemperature")
            ChildElements.ChildElements.createXMLTags(maxTemp, self.maximumTemp, self.listAbstractMeasure)

        if self.min is not None:
            minTemp = ET.SubElement(type, "minTemperature")
            ChildElements.ChildElements.createXMLTags(minTemp, self.minimumTemp, self.listAbstractMeasure)

        obsOrFcsTime_xml = ET.SubElement(type, "obsOrFcstTime")
        ET.SubElement(obsOrFcsTime_xml, "start").text = self.obsOrFcsTime

        if self.humidity is not None:
            relativeHumidity = ET.SubElement(type, "relativeHumidity")
            ChildElements.ChildElements.createXMLTags(relativeHumidity, self.relativeHumidity, self.listAbstractMeasure)

        valid_time_xml = ET.SubElement(type, "validTime")
        if len(self.validTime) == 2:
            ET.SubElement(valid_time_xml, 'duration').text = self.validTime[1]
            ET.SubElement(valid_time_xml, 'start').text = parser.parse(self.validTime[0]).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif len(self.validTime) == 1:
            ET.SubElement(valid_time_xml, 'start').text = parser.parse(self.validTime[0]).strftime("%Y-%m-%dT%H:%M:%SZ")

        if self.windDirection is not None or self.wGust is not None or self.wSpeed is not None:
            wind = None
            for component in type.iter():
                if 'wind' in component.tag:
                    wind = component
                    break

            if wind is None:
                wind = ET.SubElement(type, "wind")

        if self.windDirection is not None:
            windDirection = ET.SubElement(wind, "windDirection")
            ET.SubElement(windDirection, "maxInclusive").text = str(self.windDirection)
            ET.SubElement(windDirection, "minInclusive").text = str(self.windDirection)

        if self.wGust is not None:
            windGust = ET.SubElement(wind, "windGust")
            ChildElements.ChildElements.createXMLTags(windGust, self.windGust, self.listAbstractMeasure)

        if self.wSpeed is not None:
            windSpeed = ET.SubElement(wind, "windSpeed")
            ChildElements.ChildElements.createXMLTags(windSpeed, self.windSpeed, self.listAbstractMeasure)

    def getAtomEntry(self):
        self.initialize()
        ChildElements.ChildElements.createXMLTags(self.Entry, self.entryAtomElement, self.listAtomElement)
        links = set([('self', self.description),
                     ('up', self.parent)
                     ])
        Link.Link.createLinks(self.Entry, links)
        content = ET.SubElement(self.Entry,"content")
        type = ET.SubElement(content, "FSGIMWeatherBase")
        type.attrib["xmlns"] = "urn:X-fsgim:fsgim"
        ChildElements.ChildElements.createXMLTags(type, self.FSGIMIdentifiedObjectElements, self.listFSGIMIdentifedObjectElements)
        BaseElement.BaseElement.addBoundedBy(type, self.lowerC, self.upperC)
        ET.SubElement(type, "description").text = self.description

        WeatherBase.add_data_readings(self, type)

        return self.Entry

    def convertToKelvin(self, celcius):
        if celcius is not None:
            return str(celcius+273.15)
        else:
            return ''

    def initialize(self):
        self.listAtomElement = []
        self.listAtomElement.append('id')
        self.listAtomElement.append('title')
        self.listAtomElement.append('published')
        self.listAtomElement.append('updated')

        self.entryAtomElement = {
            'id': self.mRID,
            'title': 'FSGIM Weather Base',
            'published': self.updateTime,
            'updated': self.updateTime,
        }

        self.listFSGIMIdentifedObjectElements = []
        self.listFSGIMIdentifedObjectElements.append('mRID')
        self.listFSGIMIdentifedObjectElements.append('name')
        self.listFSGIMIdentifedObjectElements.append('nameType')

        self.FSGIMIdentifiedObjectElements = {
            'mRID': self.mRID,
            'name': self.name,
            'nameType': 'Forecast',
        }

        self.listAbstractMeasure = []
        self.listAbstractMeasure.append('value')
        self.listAbstractMeasure.append('uom')

        self.airpressure = {
            'value': str(self.pressure),
            'uom': 'pa',
        }

        self.temperature = {
            'value': self.convertToKelvin(self.air),
            'uom': 'degK',
        }

        self.dewpoint = {
            'value': self.convertToKelvin(self.dewPoint),
            'uom': 'degK',
        }

        self.maximumTemp = {
            'value': self.convertToKelvin(self.max),
            'uom': 'degK',
        }

        self.minimumTemp = {
            'value': self.convertToKelvin(self.min),
            'uom': 'degK',
        }

        self.relativeHumidity = {
            'value': str(self.humidity),
            'uom': 'none',
        }

        self.windGust = {
            'value': str(self.wGust),
            'uom': 'mPerS'
        }

        self.windSpeed = {
            'value': str(self.wSpeed),
            'uom': 'mPerS'
        }









