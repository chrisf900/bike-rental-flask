# e-Bike Rental App (Flask)

Application that allows you to rent e-Bikes. Available only in Santiago de Chile (CL) with a limited number of bikes.

Functions:
- Find e-Bikes in enabled cities.
- Request trip (start/end).
- Creation of a user profile (includes calorie tracking).


URL: http://127.0.0.1:8000/map

Documentation: 
- http://127.0.0.1:8000/docs
- http://127.0.0.1:5000/api/v1/docs
 	
## Installation

Project in Flask/Flask-RESTX and Dockerized

Run:
```
docker-compose build
docker-compose up
```

Migrate Models:
```
docker exec -it flask_app bash
flask db migrate
flask db upgrade
flask bike-rental-db create-data   *this create dummy user*
```


### **testing:**
```
docker-compose run flask_app pytest
```