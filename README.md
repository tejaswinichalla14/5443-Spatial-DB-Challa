# 5443-Spatial-DB-Challa
Name: 		Tejaswini Challa
Course:		5443 Spatial Databases
Semester:	Fall, 2022	
Assignment:	Program 1 - Simple API using python and PostgreSQL


Assignment Instructions:

  - Install Postgres DB and PostGIS
  - Install pgAdmin4
  - Created DB called Project1 using Public schema
  - Load a data file from the MSU CS server
  - Have the following API routes
    - findall
    - findone
    - near

Assignment Description:

Route 1 :
	- Routing to (findall) will fetch all the information that is stored in the db 
	
example url : http://localhost:8080/findall

Route 2 :
	- Routing to (getOne) along with appropriate parameters will fetch all the information that corresponds to that parameter 

example url :  http://localhost:8080/findone/123


Route 2 :
	- Routing to (getClosest) along with a set of latitude and longitude will fetch all the locations that are close to 
	  close to the given parameters
		

example url :  http://localhost:8080/near/40.922326/-72.637078
