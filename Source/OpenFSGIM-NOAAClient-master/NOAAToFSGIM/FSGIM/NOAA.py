import json
import requests

class NOAA:

    url = "https://api.weather.gov/"

    @staticmethod
    def getForecastDataByGridPoint(stationCode, gridPoint1, gridPoint2):
        dataUrl = NOAA.url+ 'gridpoints/' +stationCode+'/'+ gridPoint1+','+gridPoint2
        return NOAA.getDataByURL(dataUrl)

    @staticmethod
    def getObservationDataByStationID(stationID):
        dataUrl = NOAA.url+'stations/'+stationID+'/observations/current'
        return NOAA.getDataByURL(dataUrl)

    @staticmethod
    def getDataByURL(apiURL):
        dataUrl = apiURL
        response = requests.get(dataUrl)
        if response.status_code == 200:
            jsonData = json.loads(response.text)
            return jsonData
        else:
            print('     [Error]:' + response.text)


