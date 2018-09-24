import xml.etree.cElementTree as ET
from FSGIM.NOAA import NOAA
from FSGIM import WeatherBase, WeatherReport, UUIDFSGIM, UTCTime, Link, Precipitation, WeatherForecast, WeatherArea
from FSGIM import WeatherObservation
import uuid, sys
from urllib.parse import urlencode
import xml.dom.minidom
import oauth2 as oauth
import json

# Debug Code: Start

import json, time, math
from sys import platform
import getpass

debug = False
userId = getpass.getuser()
debugDir = ""

if platform == "win32" or platform == "cygwin":
     debugDir = "C:\\Users\\" + userId + "\\Dropbox\\NIST_FSGIM\\Project Deliverables\\Task3_Demonstration Files\\NOAA_Client Debugging Reports\\"

elif platform == "Linux":
    debugDir = "/home/" + userId + "/Dropbox/NIST_FSGIM/Project Deliverables/Task3_Demonstration Files/NOAA_Client Debugging Reports"

'''
Please use the following debug path as per the environment in which the application is being debugged:

where:
<username> - Please replace this with your username in the following path

---------------------------------------------------------------------------------------------------------------------------------------
For Windows 
debugDir = "C:\\Users\\<username>\\Dropbox\\NIST_FSGIM\\Project Deliverables\\Task3_Demonstration Files\\NOAA_Client Debugging Reports\\"


---------------------------------------------------------------------------------------------------------------------------------------
For Linux
debugDir = "/home/<username>/Dropbox/NIST_FSGIM/Project Deliverables/Task3_Demonstration Files/NOAA_Client Debugging Reports"
'''

#Debug Code: End

def createFeed(id):
    # Creating a feed XML element and adding the following child elements: id, title, updated and link
    feedxml = None
    feedxml = ET.Element("feed")
    feedxml.attrib["xmlns"] = "http://www.w3.org/2005/Atom"
    feedxml.attrib["xmlns:atom"] = "http://www.w3.org/2005/Atom"
    feedxml.attrib["xmlns:n1"] = "urn:X-fsgim:fsgim"
    feedxml.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
    feedxml.attrib["xsi:schemaLocation"] = "urn:X-fsgim:fsgim fsgimweather.xsd"
    uuidFeed = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, id + 'fsgimweathermodel')
    feedxml.append(UUIDFSGIM.UuidFSGIM.createUuid(uuidFeed))
    title = ET.SubElement(feedxml, "title")
    title.text = "FSGIM Weather Feed"
    update = ET.SubElement(feedxml, "updated")
    update.text = UTCTime.UTCTime.getTime()
    feedxmlLinkText = "/fsgim/1_0/resource/Weather/"
    link = Link.Link.createLink("self", feedxmlLinkText)
    return feedxml

    #------------------------------------------------------------
    #
    #  Create FSGIM Weather Forecast XML Entries
    #
    #------------------------------------------------------------

def add_forecast_data(feed_xml, forecast_data):
    sorted_weather_data = {}
    id = forecast_data['id']
    lowerCoordinates = set()
    upperCoordinates = set()
    coordinates = ((forecast_data['geometry'])['coordinates'])[0]
    max_lat = min_lat = coordinates[0][0]
    max_lon = min_lon = coordinates[0][1]

    for c in coordinates:
        max_lat = max(max_lat, c[0])
        min_lat = min(min_lat, c[0])
        max_lon = max(max_lon, c[1])
        min_lon = min(min_lon, c[1])

    lowerCoordinates.add((('coordinate'), str(min_lat)))
    lowerCoordinates.add((('coordinate'), str(min_lon)))
    upperCoordinates.add((('coordinate'), str(max_lat)))
    upperCoordinates.add((('coordinate'), str(max_lon)))

    properties = get_data('properties', forecast_data)
    update_time = get_data('updateTime', properties)
    pressure = get_data('pressure/values', properties)
    temperature = get_data('temperature/values', properties)
    dewpoint = get_data('dewpoint/values', properties)
    maxTemp = get_data('maxTemperature/values', properties)
    minTemp = get_data('minTemperature/values', properties)
    humidity = get_data('relativeHumidity/values', properties)
    windDirection = get_data('windDirection/values', properties)
    windGust = get_data('windGust/values', properties)
    windSpeed = get_data('windSpeed/values', properties)
    validTime = get_data('validTimes', properties)
    precipitation = get_data('probabilityOfPrecipitation/values', properties)

    #creating FSGIM Weather Report Component
    wReport = WeatherReport.WeatherReport(id, lowerCoordinates, upperCoordinates, update_time, validTime)
    #adding Weather Report entry element to feed element
    feed_xml.append(wReport.getEntryElement())
    LinkDataForWeatherForecast = set()

    #mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + validTime.replace("/", "%2F")
    forecast = id + '/fsgimweatherforecast/' + update_time + '/1'

    for p in pressure:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + p['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        description = id + '/' + 'fsgimweatherbase' + '/' + (p['validTime'].split("/"))[0]
        wBase = WeatherBase.WeatherBase(p['value'], None, None, None, None, update_time, None, p['validTime'],
                                        description, forecast,
                                        lowerCoordinates, upperCoordinates, None, None, None, update_time)

        sorted_weather_data.update({mRID: wBase})
        LinkDataForWeatherForecast.add(("related", description))

    for temp in temperature:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + temp['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.air = temp['value']

        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (temp['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, temp['value'], None, None, None, update_time, None, temp['validTime'],
                                            id,
                                            forecast, lowerCoordinates, upperCoordinates, None, None, None, update_time)

            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for d in dewpoint:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + d['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.dewPoint = d['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (d['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, d['value'], None, None, update_time, None, d['validTime'], id,
                                            forecast,
                                            lowerCoordinates, upperCoordinates, None, None, None, update_time)

            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for maxt in maxTemp:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + maxt['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.max = maxt['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (maxt['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, maxt['value'], None, update_time, None, maxt['validTime'],
                                            id,
                                            forecast, lowerCoordinates, upperCoordinates, None, None, None, update_time)

            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for mint in minTemp:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + mint['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.min = mint['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (maxt['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, None, mint['value'], update_time, None, mint['validTime'],
                                            description,
                                            forecast, lowerCoordinates, upperCoordinates, None, None, None, update_time)

            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for h in humidity:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + h['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            if mRID in sorted_weather_data:
                present_component = sorted_weather_data[mRID]
                present_component.humidity = h['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (h['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, None, None, update_time, h['value'], h['validTime'],
                                            description,
                                            forecast, lowerCoordinates, upperCoordinates, None, None, None, update_time)

            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for windD in windDirection:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + windD['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.windDirection = windD['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (windD['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, None, None, update_time, None, windD['validTime'],
                                            description, forecast,
                                            lowerCoordinates, upperCoordinates, windD['value'], None, None, update_time)
            wBaseEntry = wBase.getAtomEntry()
            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for windG in windGust:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + windG['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.wGust = windG['value']



        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (windG['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, None, None, update_time, None, windG['validTime'],
                                            description, forecast,
                                            lowerCoordinates, upperCoordinates, None, windG['value'], None, update_time)
            #wBaseEntry = wBase.getAtomEntry()
            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for windS in windSpeed:
        mrid_string = id + '/' + 'fsgimweatherbase' + '/' + update_time + '/' + windS['validTime'].replace("/", "%2F")
        mRID = UUIDFSGIM.UuidFSGIM.generate(uuid.NAMESPACE_URL, mrid_string)
        present_component = None

        if mRID in sorted_weather_data:
            present_component = sorted_weather_data[mRID]
            present_component.wSpeed = windS['value']
        else:
            description = id + '/' + 'fsgimweatherbase' + '/' + (windS['validTime'].split("/"))[0]
            wBase = WeatherBase.WeatherBase(None, None, None, None, None, update_time, None, windS['validTime'],
                                            description, forecast,
                                            lowerCoordinates, upperCoordinates, None, None, windS['value'], update_time)
            #wBaseEntry = wBase.getAtomEntry()
            sorted_weather_data.update({mRID: wBase})
            LinkDataForWeatherForecast.add(("related", description))

    for key, value in sorted_weather_data.items():
        feed_xml.append(value.getAtomEntry())

    for p in precipitation:
        description = id + '/' + 'fsgimweatherbase' + '/' + (p['validTime'].split("/"))[0]
        precip = Precipitation.Precipitation(p['value'], p['validTime'], description, forecast, lowerCoordinates,
                                             upperCoordinates)
        precipitationEntry = precip.getAtomEntry()
        feed_xml.append(precipitationEntry)
        LinkDataForWeatherForecast.add(("related", description))

    forecastElement = WeatherForecast.WeatherForecast(validTime, id, update_time, LinkDataForWeatherForecast)
    feed_xml.append(forecastElement.getAtomEntry())
    weatherArea = WeatherArea.WeatherArea(id, lowerCoordinates, upperCoordinates, forecast, update_time, validTime)
    feed_xml.append(weatherArea.getAtomEntry())
    return feed_xml

def get_data(property_name, forecast_data):
    #   This function checks if 'property_name' value exists in the 'forecast_data' retrieved from NOAA.

    #   If the relevant data exists then respective values are returned.

    #   This is a safe way to retrieve data from a nested dictionary data structure.

    if forecast_data is not None:
        try:
            properties = property_name.split('/')
            data = forecast_data
            for p in properties:
                if p in data:
                    data = data.get(p)
                else:
                    raise Exception()
            return data

        except Exception:
            print("\n[Error]: "+property_name+" doesn't exists in the response received from NOAA.")
            return None

    #------------------------------------------------------------
    #
    #  Create FSGIM Weather Observation XML Entries
    #
    #------------------------------------------------------------

def addWeatherObservation(feedxml, observationData):
    properties = get_data('properties', observationData)
    pressure = get_data('barometricPressure/value', properties)
    airTemp = get_data('temperature/value', properties)
    dewpoint = get_data('dewpoint/value', properties)
    maxTemp = get_data('maxTemperatureLast24Hours/value', properties)
    minTemp = get_data('minTemperatureLast24Hours/value', properties)
    if 'precipitationLastHour' in properties:
        precipitationLasthr = get_data('precipitationLastHour/value', properties)
    obsOrfcsTime = observationData['id']
    urlParts = obsOrfcsTime.split('/')
    obsOrfcsTime = urlParts[6]
    humidity = get_data('relativeHumidity/value', properties)
    windDirection = get_data('windDirection/value', properties)
    windSpeed = get_data('windSpeed/value', properties)
    windGust = get_data('windGust/value', properties)
    validTime = get_data('timestamp', properties)
    updateTime = validTime

    # domainparts = urlParts[2].split('.')
    # urlParts[2] = '.'.join(domainparts[1:3])
    # description = '/'.join(urlParts[2:7])
    id = observationData['id']
    description = observationData['id']
    observationSelf = observationData['id']

    wbDescription = observationData

    position = get_data('geometry/coordinates', observationData)
    positionCoordinates = set()

    for p in position:
        positionCoordinates.add((('coordinate'), p))

    LinkDataForWeatherObservation = set()

    #creating FSGIM Weather Report Component
    wReport = WeatherReport.WeatherReport(id, positionCoordinates, positionCoordinates, updateTime, validTime)
    feedxml.append(wReport.getEntryElement())
    report_link = id + '/fsgimweatherreport/' + updateTime
    LinkDataForWeatherObservation.add(('related', report_link))

    description = id + '/' + 'fsgimweatherbase'
    LinkDataForWeatherObservation.add(('related', description))
    wbElement = WeatherBase.WeatherBase(pressure, airTemp, dewpoint, maxTemp, minTemp, obsOrfcsTime, humidity, validTime,
                                        description, observationSelf, positionCoordinates, positionCoordinates, windDirection, windGust, windSpeed, updateTime)
    feedxml.append(wbElement.getAtomEntry())

    if 'precipitationLastHour' in properties and precipitationLasthr is not None:
        wPrecipitation = Precipitation.Precipitation(precipitationLasthr, '/PT1H', observationSelf, observationSelf, positionCoordinates, positionCoordinates)
        feedxml.append(wPrecipitation.getAtomEntry())

    area_link = id + '/fsgimweatherarea/' + updateTime
    LinkDataForWeatherObservation.add(('related', area_link))

    observation_self = id + '/fsgimweatherobservation/' + updateTime
    LinkDataForWeatherObservation.add(('self', observation_self))
    observation_element = WeatherObservation.WeatherObservation(id, LinkDataForWeatherObservation, updateTime, validTime)
    feedxml.append(observation_element.getAtomEntry())

    weatherArea = WeatherArea.WeatherArea(id, positionCoordinates, positionCoordinates, observationSelf, updateTime, validTime)
    feedxml.append(weatherArea.getAtomEntry())

def weatherDataByLocation(latitude, longitude):
    metadataUrl = 'https://api.weather.gov/points/' + str(latitude) + ',' + str(longitude)
    try:
        metadata = NOAA.getDataByURL(metadataUrl)
        forecastGridDataURL = metadata['properties']['forecastGridData']
        forecastData = NOAA.getDataByURL(forecastGridDataURL)
        observationStationsURL = metadata['properties']['observationStations']
        osResponseData = NOAA.getDataByURL(observationStationsURL)
        stationIdentifier = osResponseData['features'][0]['properties']['stationIdentifier']
        observationData = NOAA.getObservationDataByStationID(stationIdentifier)
        return forecastData, observationData
    except:
        print("     [Error]: Cannot retrieve data from NOAA Weather API.")
        return False

def coordinatesFromAddress(location, apiKey):
    '''This function uses Google map API to calculate latitude and longitude of an address.'''
    try:
        serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

        # Debug code: start
        if(debug and apiKey is None):
            url = serviceurl + urlencode(
                {'sensor': 'false', 'address': location})
        # Debug code: end
        else:
            url = serviceurl + urlencode(
                {'sensor': 'false', 'address': location, 'key': apiKey})

        googlemaps_location = NOAA.getDataByURL(url)

        if(googlemaps_location['status'] == 'OK'):
            lat = googlemaps_location['results'][0]['geometry']['location']['lat']
            lon = googlemaps_location['results'][0]['geometry']['location']['lng']
            return lat, lon, 'OK'
        else:
            return "", "", googlemaps_location['status']

    except:
        print("[Error]: Cannot retrieve geographical coordinates from Google geocoding API.")

def printErrorMessage(apiKey, location, requestType):
    print("\n[Error]: Invalid input!\n\t\t| APIKey: " + str(apiKey) + "\n\t\t| Location: " + str(location)
                            + "\t\t| Request Type: " + str(requestType) + "\n")
    print("\t\tPlease use the following format to run this application:")
    print("\t\t\t>python run.py 'APIKey' 'Location or Address' 'Request Type'\n")
    print("\t\tThe following input is required:")
    print("\t\t\t1.'APIKey': Please use a Google geocode API key.")
    print("\t\t\t2.'Location or Address': Please enter location for which the application will collect data from NOAA.")
    print("\t\t\t3.'Request Type': Please select a valid value for this input: 'forecast' or 'observation'.")

# Debug code: start
def writeOnFile(id, requestType, jsonData, feedXml):
    idSplit = id.split("//")
    idSplit[1] = idSplit[1].replace("/", ".")
    output = ET.tostring(feedXml, method="xml")
    parsedXml = xml.dom.minidom.parseString(output)
    pretty_xml_as_string = parsedXml.toprettyxml()
    timeSeconds = str(math.ceil(time.time()))
    debugJsonPath = debugDir + 'NOAA'+requestType+'Response.' + timeSeconds + "." + idSplit[1] + ".json"
    debugXMLpath = debugDir + 'NOAA'+requestType+'APIResponseGeneratedXMLFile.' + timeSeconds + "." + idSplit[1]+".xml"
    try:
        jsonFile = open(debugJsonPath, 'w+')
        jsonFile.write(jsonData)
        jsonFile.close()
        xmlFile = open(debugXMLpath, 'w+')
        xmlFile.write(pretty_xml_as_string)
        xmlFile.close()
    except Exception as e:
        print("\n[Error]: Debug Mode: Application was not able to write the results on the file.")
        print("\n[Error]: " + str(e))
# Debug code: end

def post_data(post_url, data):
    Consumer_key = ""
    Consumer_secret = ""

    access_token = ""
    access_token_secret = ""

    consumer = oauth.Consumer(key=Consumer_key, secret=Consumer_secret)
    access_token = oauth.Token(key=access_token, secret=access_token_secret)
    client = oauth.Client(consumer, access_token)
    response, content = client.request(
        post_url,
        method="POST",
        body=data,
        headers={'Content-type': 'application/xml',
                 'grant_type': 'client_credentials'}
    )

def main(location, apiKey, requestType):
    if len(location) >= 5 and len(requestType) != 0:

        lat, lon, status = coordinatesFromAddress(location, apiKey)
        if status == "OK":
            forecastData, observationData = weatherDataByLocation(lat, lon)
            try:
                id = forecastData['id']
                feedXml = createFeed(id)
                if requestType.lower() == 'forecast':
                    add_forecast_data(feedXml, forecastData)
                    # post_data('', feedXml)
                    # Debug code: start
                    # The following code has to be removed before project completion.
                    if debug:
                        print("NOAA Forecast Response " + id)
                        writeOnFile(id,
                                    requestType,
                                    (json.dumps(forecastData, indent=4)),
                                    feedXml)
                        # Debug code: end
                elif requestType.lower() == 'observation':
                    addWeatherObservation(feedXml, observationData)
                    # post_data('', feedXml)
                    # Debug code: start
                    # The following code has to be removed before project completion.
                    if debug:
                        print("NOAA Observation Response " + id)
                        writeOnFile(id,
                                    requestType,
                                    (json.dumps(observationData, indent=4)),
                                    feedXml)
                        # Debug code: end

                else:
                    printErrorMessage(apiKey, location, requestType)
            except Exception as e:
                print("\n[Error]: " + str(e))
        else:
            if(status == "ZERO_RESULTS"):
                message = " -- indicates the Google API request was successful but returned no results." \
                          " This may occur if the Google API request was passed a non-existent address."

            elif(status == "OVER_QUERY_LIMIT"):
                message = " -- indicates you have exceeded your Google API request quota."

            elif(status == "REQUEST_DENIED"):
                message = " -- indicates the Google API request was denied."

            elif(status == "INVALID_REQUEST"):
                message = " -- generally indicates the Google API request (address, components or latlng) is missing."

            elif(status == "UNKNOWN_ERROR"):
                message = " -- indicates the Google API request could not be processed due to a server error." \
                          " The request may succeed if you try again."

            else:
                message = " -- received an undocumented Status from the Google geocoding API"

            raise sys.exit ("\n[Error]: " + status + message)

                #Code for OAuth 2.0 to be added here

    else:
        printErrorMessage(apiKey, location, requestType)


apiKey = ""
location = ""
requestType = ""
try:
    config = open('Config.json')
    config_data = json.load(config)
    debug = get_data('debug', config_data)
    apiKey = get_data('api_key', config_data)
except Exception as e:
    print("\n[Error]: Config file Error")
    print("\n[Error]: " + str(e))

if len(sys.argv) == 4 or debug:
    
    if not debug:
        apiKey = sys.argv[1]
        location = sys.argv[2]
        requestType = sys.argv[3]
    else:
        location = input("Enter Location: ")
        requestType = input("Enter Request Type: ")

    main(location, apiKey, requestType)
else:
    printErrorMessage(apiKey, location, requestType)
















