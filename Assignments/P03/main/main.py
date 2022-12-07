import time
import requests
import json

url = "http://missilecommand.live:8080/REGISTER"

if __name__=='__main__':
    while(True):
        time.sleep(1)
        r = requests.get(url)
        response = requests.get("http://missilecommand.live:8080/REGISTER")

        print(r.text)