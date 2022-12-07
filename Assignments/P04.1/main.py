import psycopg2
import json
from geojson import Polygon, Point


class DBCursor(object):
    def __init__(self, config):
        with open(config) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["DbName"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.cur = self.conn.cursor()

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


with DBCursor("config.json") as cur:
    cur.execute(open("SQL/ships.psql", "r").read())

boatsCount = 0

with open("ships.json", "r") as shipsFile:
    ships = json.load(shipsFile)

    insert = "INSERT INTO public.ships(id, category, shipclass, length, width, torpedolaunchers, armament, hullarmor, deckarmor, speed, turnradius, location, bearing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    for ship in ships:
        row = [ship["id"], ship["category"], ship["shipClass"], ship["length"], ship["width"]]
        row.append(ship["torpedoLaunchers"]) if ship["torpedoLaunchers"] is None else row.append(
            json.dumps(ship["torpedoLaunchers"]))
        row.append(json.dumps(ship["armament"]))
        row.append(ship["armor"]["hull"])
        row.append(ship["armor"]["deck"])
        row.append(ship["speed"])
        row.append(ship["turn_radius"])
        row.append(ship["location"])
        row.append(0.0)

        with DBCursor("config.json") as cur:
            cur.execute(insert, row)

        boatsCount += 1

# Choosing a Direction
degrees = 60

cardinalList = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
cardinalDegree = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
cardinalMax = [348.75, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75,
               281.25, 303.75, 326.25]
cardinalMin = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25,
               303.75, 326.25, 348.75]

index = int((degrees + 11.25) / 22.5)

direction = cardinalList[index % 16]
opposite = cardinalList[(index + 8) % 16]
oppositeBearing = cardinalDegree[(index + 8) % 16]

left = cardinalMax[index % 16]
right = cardinalMin[index % 16]

bbox = {
    "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
    "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
}
bbox = f"""SELECT ST_AsGeoJson(ST_MakeEnvelope({bbox['UpperLeft']['lon']}, {bbox['LowerRight']['lat']},  {bbox['LowerRight']['lon']}, {bbox['UpperLeft']['lat']}, 4326))"""
with DBCursor("config.json") as cur:
    cur.execute(bbox)
    bbox = Polygon(json.loads(cur.fetchall()[0][0])["coordinates"])

centerOfBBox = "SELECT ST_AsGeoJson(ST_Centroid(ST_GeomFromGeoJSON('" + str(bbox) + "')))"

with DBCursor("config.json") as cur:
    cur.execute(centerOfBBox)
    Center = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

# Creating Reference Points , Basing these other boats are placed

referencePoint1 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(
    Center) + "'), 80000, radians(" + str(
    left) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with DBCursor("config.json") as cur:
    cur.execute(referencePoint1)
    referencePoint1 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

referencePoint2 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(
    Center) + "'), 80000, radians(" + str(
    right) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with DBCursor("config.json") as cur:
    cur.execute(referencePoint2)
    referencePoint2 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

update = "UPDATE ships SET location = ST_GeomFromGeoJSON(%s), bearing = " + str(oppositeBearing) + " WHERE id = %s"

# Placing Boats
boat0 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    referencePoint1) + "'), 111, radians(270)), 111, radians(0)))"
with DBCursor("config.json") as cur:
    cur.execute(boat0)
    boat0 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat02 = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(referencePoint1) + "'), 111, radians(270)))"
with DBCursor("config.json") as cur:
    cur.execute(boat02)
    boat02 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat03 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    boat02) + "'), 111, radians(270)), 111, radians(180)))"
with DBCursor("config.json") as cur:
    cur.execute(boat03)
    boat03 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat04 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    boat0) + "'), 111, radians(270)), 111, radians(180)))"
with DBCursor("config.json") as cur:
    cur.execute(boat04)
    boat04 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat05 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    boat04) + "'), 111, radians(270)), 111, radians(180)))"
with DBCursor("config.json") as cur:
    cur.execute(boat05)
    boat05 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat06 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    referencePoint1) + "'), 111, radians(270)), 111, radians(180)))"
with DBCursor("config.json") as cur:
    cur.execute(boat06)
    boat06 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat07 = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(referencePoint1) + "'), 111, radians(180)))"
with DBCursor("config.json") as cur:
    cur.execute(boat07)
    boat07 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

boat08 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(
    boat0) + "'), 0, radians(0)), 111, radians(270)))"
with DBCursor("config.json") as cur:
    cur.execute(boat08)
    boat08 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat02), 0))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat03), 1))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat0), 2))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat04), 3))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat05), 4))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat06), 5))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat07), 6))

with DBCursor("config.json") as cur:
    cur.execute(update, (json.dumps(boat08), 7))

final_output = {
    "fleet_id": "BrahMos",
    "ship_status": []
}

# Choosing ID Bearing and location from created boats
final_query = "SELECT id, bearing, ST_asGeoJSON(location) FROM ships ORDER BY id ASC limit 8"
with DBCursor("config.json") as cur:
    cur.execute(final_query)
    results = cur.fetchall()

for result in results:
    final_output["ship_status"].append({"ship_id": result[0], "bearing": result[1],
                                        "location": {"lon": json.loads(result[2])["coordinates"][0],
                                                     "lat": json.loads(result[2])["coordinates"][1]}})

with open("final_product.json", "w") as out:
    print(final_output)
    json.dump(final_output, out, indent=4)
