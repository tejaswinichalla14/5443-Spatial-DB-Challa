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


outfile = open("Query_Results.txt", "w")

queryForGunStateTable = "SELECT * FROM gun_state WHERE ship_id = 6 and gun_id = 'Mark11'"

with DBCursor("config.json") as cur:
    cur.execute(queryForGunStateTable)
    output = cur.fetchall()

outfile.write("Before: " + str(output) + '\n\n')

updateAmmo = "UPDATE gun_state SET ammo = 111  where ship_id = 6 and gun_id = 'Mark11'"
outfile.write("Query: " + updateAmmo + '\n\n')

with DBCursor("config.json") as cur:
    cur.execute(updateAmmo)

with DBCursor("config.json") as cur:
    cur.execute(queryForGunStateTable)
    output = cur.fetchall()

outfile.write("After updating the ammo: " + str(output) + '\n\n')
outfile.write("********************************************************************************************************" '\n\n')

queryForShipState = "SELECT * FROM ship_state WHERE ship_id = 6"
updateSpeedAndDirection = "UPDATE ship_state SET bearing = 300, speed = 70 WHERE ship_id = 6"

with DBCursor("config.json") as cur:
    cur.execute(queryForShipState)
    output = cur.fetchall()

outfile.write("Before: " + str(output) + '\n\n')
outfile.write("Query: " + updateSpeedAndDirection + '\n\n')

with DBCursor("config.json") as cur:
    cur.execute(updateSpeedAndDirection)

with DBCursor("config.json") as cur:
    cur.execute(queryForShipState)
    output = cur.fetchall()

outfile.write("After updating speed and direction: " + str(output) + '\n\n')
outfile.write("*************************************************************************************************************"'\n\n')


queryForGunStateTable = "SELECT ship_id, gun_id, bearing FROM gun_state WHERE ship_id = 7"
updateDirection = "UPDATE gun_state SET bearing = 111 WHERE ship_id = 7"

with DBCursor("config.json") as cur:
    cur.execute(queryForGunStateTable)
    output = cur.fetchall()

outfile.write("Before: " + str(output) + '\n\n')
outfile.write("Query: " + updateDirection + '\n\n')

with DBCursor("config.json") as cur:
    cur.execute(updateDirection)

with DBCursor("config.json") as cur:
    cur.execute(queryForGunStateTable)
    output = cur.fetchall()

outfile.write("After updating direction: " + str(output) + '\n\n')
outfile.write("*************************************************************************************************************"'\n\n')

