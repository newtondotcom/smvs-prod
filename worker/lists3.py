import requests
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get("API_KEY")
s3s = []

def get_list():
    global s3s
    url = 'http://localhost:3000/api/s3/list'
    headers = {
        'Authorization': 'Bearer '+apikey
    }
    response = requests.get(url, headers=headers)
    s3s = response.json()


get_list()

def get_s3(name):
    for s3 in s3s:
        if s3['name'] == name:
            return s3
    return None