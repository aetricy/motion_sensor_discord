import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def make_request(url):
    try:
        response=requests.get(url,timeout=0.5)
    except ConnectTimeout:
        print('Request has timed out = '+url)

def status():
   
    try:
        response=requests.get("http://192.168.1.254:255/status",timeout=0.5)
    except ConnectTimeout:
        print('Request has timed out')

    root = ET.fromstring(response.content)
    distance = root.find("ds").text
    alarm= root.find("al").text
    toggle=root.find("wk").text

    return [distance,alarm,toggle]

status()