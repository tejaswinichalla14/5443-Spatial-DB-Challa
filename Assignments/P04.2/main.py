import psycopg2
import json


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
    cur.execute(open("SQL/Tables/cartridge.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/gun.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/gun_state.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/projectile.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/gun_state.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/ship_guns.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/ship_state.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/torpedo.psql", "r").read())

with DBCursor("config.json") as cur:
    cur.execute(open("SQL/Tables/torpedo_state.psql", "r").read())

ships = "SELECT * FROM ships"
with DBCursor("config.json") as cur:
    cur.execute(ships)
    ships = cur.fetchall()

queryForShipState = "INSERT INTO public.ship_state(ship_id, bearing, speed, location) VALUES (%s, %s, %s, %s);"
queryForShipGun = "INSERT INTO public.ships_guns(ship_id, gun_id, type, pos) VALUES (%s, %s, %s, %s);"
queryForGunState = "INSERT INTO public.gun_state(ship_id, gun_id, bearing, elevation, ammo) VALUES (%s, %s, %s, %s, %s);"
queryForTorpedoState = "INSERT INTO public.torpedo_state(ship_id, t_id, location, side, facing) VALUES (%s, %s, %s, %s, %s);"


for ship in ships:
    with DBCursor("config.json") as cur:
        cur.execute(queryForShipState, (ship[0], ship[12], ship[9], ship[11]))

    for armory in ship[6]:
        with DBCursor("config.json") as cur:
            cur.execute(queryForShipGun,
                        (ship[0], armory['gun']['name'], armory['gun']['ammoType'][0], armory['pos']))

        with DBCursor("config.json") as cur:
            cur.execute(queryForGunState,
                        (ship[0], armory['gun']['name'], ship[12], 0, armory['gun']['ammo'][0]['count']))

    if ship[5] is not None:
        for torpedo in ship[5]:
            with DBCursor("config.json") as cur:
                cur.execute(queryForTorpedoState, (
                    ship[0], torpedo['torpedos']['name'], torpedo['location'], torpedo['side'], torpedo['facing']))

print("Tables Created Successfully")
