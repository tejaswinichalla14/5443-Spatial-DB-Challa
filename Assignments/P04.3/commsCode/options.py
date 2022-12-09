import http.client
import requests
import json



HASH_KEY = ""
FLEETNAME = "Brahmos"

GAME_ID = 0

def start_game():
    url = f"https://battleshipgame.fun:8080/generate_fleet/?fleetName={FLEETNAME}&hash={HASH_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    if response.ok == True:
        print("Game has been started!!")
    else:
        print("Error game was unable to start :(")

def generate_fleet():
    url = f"https://battleshipgame.fun:8080/generate_fleet/?fleetName={FLEETNAME}&hash={HASH_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    if response.ok:
        with open("ships.json", "w") as file:
            json.dump(data, file, indent=4)
        return data
    else:
        return "ERROR!!!!"    
    
def create_game():
    url = f"https://battleshipgame.fun:8080/create_game/?hash={HASH_KEY}&game_name={FLEETNAME}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print({"Game information": response.json()})



