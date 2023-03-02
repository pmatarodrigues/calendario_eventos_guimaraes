import requests
import urllib3

def getHTMLdoc(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)

    return response.text