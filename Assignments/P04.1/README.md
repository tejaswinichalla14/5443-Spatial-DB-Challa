P04.1 - BS: Ship Location Generation

# Description:
This project takes in a json file of ships and positions them in a fleet by using PSQL for storing and PostGIS for calculations.


#	File/folder	Description
1	main.py	- 
Main file of the project that places the ships in a fleet by making appropriate calculations such that the each ship is spaced out 222m from bow to stern from each other and 111m from port to starboard

2	SQL	- 
SQL files that make the tables, adds indexes, and other useful sql


3	ships.json - 
json file containing all ships we have in the fleet

4	final_product.json	- 
json file containing all information such as bearing and location of each ship after placing them in a fleet 
