from fastapi import FastAPI
from pydantic import BaseModel  
from fastapi.responses import RedirectResponse
import uvicorn
import psycopg2
import json
import random
import requests
# from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2

import time

# from module import DatabaseCursor
# from module import DBQuery


# class MissileSol(BaseModel):
#     id:   str   
#     time: int   
#     mid:  int   
#     lon1: float 
#     lat1: float 
#     alt1: float 
#     lon2: float 
#     lat2: float
#     alt2: float 

app = FastAPI()

class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["dbname"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "host='"
            + self.conn_config["host"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()

class DBQuery(object):
    def __init__(self, config):
        self.result = {}
        self.config = config
        self.limit = 1000
        self.offset = 0

    def __query(self, sql, qtype=3):
        with DatabaseCursor(self.config) as cur:
            print(sql)
            cur.execute(sql)

            if qtype == 1:
                self.result["data"] = cur.fetchone()
            elif qtype == 2:
                self.result["data"] = cur.fetchmany()
            else:
                self.result["data"] = cur.fetchall()

            self.result["limit"] = self.limit
            self.result["offset"] = self.offset
            self.result["sql"] = sql
            self.result["success"] = cur.rowcount > 0
            self.result["effectedRows"] = cur.rowcount
        return self.result

    def queryOne(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}")

    def queryAll(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}")

    def queryMany(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit
        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}")

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

    # cleanResult = {
    #     "lon1":res['data'][0],
    #     "lat1":res['data'][1],
    #     "lon2":res['data'][2],
    #     "lat2":res['data'][3]
    # }

    # res['data'] = cleanResult

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
        "l": -124.7844079, 
        "r": -66.9513812,  
        "t": 49.3457868,    
        "b": 24.7433195,   
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


@app.get("/radar_sweep")
def radar_sweep(cat:str):
    sql = f"""SELECT * FROM missile_blast
    WHERE cat = {cat}
    """
   
    res = conn.queryMany(sql)

    return res
    


@app.get("/numRegions")
def region():
    sql = "SELECT distinct(gid) FROM regions ORDER BY gid"
    res = conn.queryMany(sql)

    return res


@app.get("/region")
def region(gid: int, cid: int):


    sql = f"""
    SELECT newgeom::json as region FROM public.regions_simple 
    WHERE gid = {gid} AND cid = {cid}
    """

    res = conn.queryOne(sql, noPagination=True)



    fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": res["data"][0][0]["type"],
                    "coordinates": res["data"][0][0]["coordinates"],
                },
            }
        ],
    }

    return fc


@app.get("/missileInfo")
def missileInfo(name: str = None):

    where = ""

    if name:
        where = f"""WHERE "missile"."name" like '{name}'"""

    sql = f"""
        SELECT
        missile.name,
        missile_speed.ms,
        missile_blast.blast_radius
        FROM
        missile
        INNER JOIN missile_speed ON "missile"."speedCat" = missile_speed.category
        INNER JOIN missile_blast ON "missile"."blastCat" = missile_blast.cat
        {where}
    """

    res = conn.queryMany(sql)

    returnVals = []

    for row in res['data']:
        returnVals.append({"name":row[0],"speed":row[1],"blast":row[2]})

    return returnVals


@app.get("/missileSolution/")
async def getSolution(id:str):
    sql = f"SELECT * FROM public.missile WHERE id = {id}"
    res = conn.queryMany(sql)
    return res
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)