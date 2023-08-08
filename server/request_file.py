import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def make_request(url):
    try:
        response=requests.get(url,timeout=0.5)
        return 200
    except ConnectTimeout:
        print('Request has timed out = '+url)
        return 502

def status():
   
    try:
        response=requests.get("http://192.168.1.254:255/status",timeout=0.5)
        root = ET.fromstring(response.content)
        distance = int(root.find("ds").text)
        alarm= int(root.find("al").text)
        toggle=int(root.find("wk").text)
        return [distance,alarm,toggle]
    except ConnectTimeout:
        return 502

  

    

