
from flask import Flask
import psycopg2
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello people'
@app.route("/findall")
def getPage():
    cursor.execute('''select * from public."Earthquakes"''')
    data = cursor.fetchall()
    return data

@app.route("/findone/<num>")
def id(num):
    num = str(num);
    cursor.execute('SELECT * FROM public."Earthquakes" WHERE id = ''' + num + '')
    data = cursor.fetchall()
    return data    

@app.route('/near/<depth>/<magnitude>')
def closest(depth, magnitude):
    depth = str(depth);
    magnitude = str(magnitude);
    cursor.execute('SELECT  * FROM public."Earthquakes" WHERE depth = ''' + depth + ' OR magnitude = ''' + magnitude + '')
    data = cursor.fetchall()
    return data

connect = psycopg2.connect(database="Project1", user='postgres', password='admin')
cursor = connect.cursor()

if __name__ == '__main__':
    app.run(debug=True, port='8080')

