import requests
import urllib3

class EventScrapper:
    @classmethod
    def getHTMLdoc(cls, url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, verify=False)

        return response.text
