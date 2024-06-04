import requests
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get("API_KEY")
s3s = []
url = "https://app.yogocap.com/api/s3/list"

def get_list():
    global s3s
    headers = {
        'Authorization': 'Bearer '+apikey
    }
    response = requests.get(url, headers=headers)
    s3s = response.json()
    print("S3 list updated")


get_list()

def get_s3(name):
    for s3 in s3s:
        if s3['name'] == name:
            return s3
    return None