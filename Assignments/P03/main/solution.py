from fastapi import FastAPI
from pydantic import BaseModel  
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json
import random
from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2

import time

from module import DatabaseCursor
from module import DBQuery

class MissileSol(BaseModel):
    id:   str  
    time: int
    mid:  int
    lon1: float
    lat1: float
    alt1: float
    lon2: float
    lat2: float
    alt2: float

app = FastAPI()


conn = DBQuery(".config.json")



@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/missileNext")
def missileNext(lon:float=-98.12345, lat:float=34.2345, speed:float=333, bearing:float=270, time:int=1, drop:float=0.0 , geojson:bool=False):
    """
    lon (float) : x coordinate
    lat (float) : y coordinate
    speed (int) : meters per second
    bearing (float) : direction in degrees (0-360)
    """
    if not geojson:
        select = "lon1 as x1, lat1 as y1, st_x(p2) as x2,st_y(p2) as y2"
    else:
        select = "ST_AsGeoJSON(p2)"

    sql = f"""
    WITH 
        Q1 AS (
            SELECT {lon} as lon1,{lat} as lat1, ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({bearing}))::geometry,4326) as p2
        )
 
    SELECT {select}
    FROM Q1
    """

    print(sql)

    res = conn.queryOne(sql)

    cleanResult = {
        "lon1":res['data'][0],
        "lat1":res['data'][1],
        "lon2":res['data'][2],
        "lat2":res['data'][3]
    }

    res['data'] = cleanResult

    return res


@app.get("/missile_path")
def missilePath(d: str = None, buffer: float = 0):
    """ Returns a missile path across the entire continental US 
        **Not sure how necessary this is:)**
    ### Params:
        d (str) : direction of missile, if None then it will be random
        buffer (float) : a padding added to or from the bbox (Cont US)
    ### Returns:
        [float,float] start and end
    """
    bbox = {
        "l": -124.7844079,  # left
        "r": -66.9513812,   # right
        "t": 49.3457868,    # top
        "b": 24.7433195,    # bottom
    }

    directions = ["N", "S", "E", "W"]

    if not d:
        d = random.shuffle(directions)

    x1 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    x2 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    y1 = (abs(bbox["t"])  - abs(bbox["b"])) * random.random() + abs(bbox["b"])
    y2 = (abs(bbox["t"])  - abs(bbox["b"])) * random.random() + abs(bbox["b"])

    if d == "N":
        start = [x1, bbox["b"] - buffer]
        end = [x2, bbox["t"] + buffer]
    elif d == "S":
        start = [x1, bbox["t"] + buffer]
        end = [x2, bbox["b"] - buffer]
    elif d == "E":
        start = [bbox["l"] - buffer, y1]
        end = [bbox["r"] + buffer, y2]
    else:
        start = [bbox["r"] + buffer, y1]
        end = [bbox["l"] - buffer, y2]

    return [start, end]


@app.get("/missileInfo")
def missileInfo(name: str = None):
    """Get the speed and blast radius for the arsenal of missiles.
    ### Params:
        name (str) : filter the results to match name. Otherwise all missiles are returned.
    ### Returns:
        (list) : one or all missiles
    """

    where = ""

    if name:
        where = f"WHERE missile.name like '{name}'"

    sql = f"""
        SELECT
        missile.name,
        missile_speed.ms,
        missile_blast.blast_radius
        FROM
        missile
        INNER JOIN missile_speed ON missile.speed_cat = missile_speed.cat
        INNER JOIN missile_blast ON missile.blast_cat = missile_blast.cat
        {where}
    """

    print(sql)

    res = conn.queryMany(sql)

    returnVals = []

    for row in res['data']:
        returnVals.append({"name":row[0],"speed":row[1],"blast":row[2]})

    return returnVals


@app.get("/missileSolution/")
async def getSolution(id:str):
    sql = f"SELECT * FROM public.missile_solution WHERE id like '{id}'"
    res = conn.queryMany(sql)
    return res

@app.post("/missileSolution/")
async def postSolution(ms: MissileSol):


    sql = f"""INSERT INTO public.missile_solution(
        id, "time", mid, lon1, lat1, alt1, lon2, lat2, alt2)
        VALUES ('{ms.id}', {ms.time}, {ms.mid}, {ms.lon1}, 
        {ms.lat1}, {ms.alt1}, {ms.lon2}, {ms.lat2}, {ms.alt2});"""

    res = conn.queryPost(sql)
    return res

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, log_level="debug", reload=True)