from flask import Flask
import psycopg2
app=Flask(__name__)
@app.route('/')
def hello():
   return "hello, there"
   
#finding all data   
@app.route("/findall")
def getPage():
    cursor.execute('''select * from public."Earthquakes"''')
    data = cursor.fetchall()
    return data

#finding specific id
@app.route("/findone/<num>")
def id(num):
    num = str(num);
    cursor.execute('SELECT distinct * FROM public."Earthquakes" WHERE id = ''' + num + '')
    data = cursor.fetchall()
    return data  

#finding data with given depth
@app.route("/depth/<num>")
def depth(num):
    num = str(num);
    cursor.execute('SELECT distinct * FROM public."Earthquakes" WHERE depth = ''' + num + '')
    res = cursor.fetchall()
    return res  

#finding data with given magnitude
@app.route("/magnitude/<num>")
def magnitude(num):
    num = str(num);
    cursor.execute('SELECT distinct * FROM public."Earthquakes" WHERE magnitude = ''' + num + '')
    mag = cursor.fetchall()
    return mag      

#finding closest locations based on latitude and longitude
@app.route('/near/<latitude>/<longitude>')
def closest(latitude, longitude):
    latitude = str(latitude);
    longitude = str(longitude);
    cursor.execute('SELECT distinct ST_Distance( ST_Closestpoint( st_setSRID(r.geom,4326), st_setSRID(ST_makePOINT(51.096, -179.392),4326) ), ST_makePOINT('+ latitude +', '+ longitude +') ,true ) as distance, r.id, r.occured, r.latitude, r.longitude, r.depth, r.magnitude, r.place, r.cause FROM public."Earthquakes" r ORDER BY distance LIMIT 5')
    data = cursor.fetchall()
    return data
    
#connection to postgres
connect = psycopg2.connect(database="postgres", user='postgres', password='admin')
cursor = connect.cursor()

if __name__ == '__main__':
    app.run(debug=True, port='8080')

