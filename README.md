# CarsApi: A simple REST API for cars
CarsAPI is a RESTful API designed for users to manage cars.

# Authentication

* Access is granted to authenticated users via JSON Web Tokens (JWTs).

# Permissions
* Besides the superuser, CarsApi users can be assigned two roles: Admin or Client.
* The API data are manyfold. A user with credentials can access details of users, cars, brands and models.
## Users
* To be created, a user must register on the API at the following endpoint  (make sure the local server is running): [http://localhost:8000/api/v1/register/](http://localhost:8000/api/v1/register/)
* Initially, a user has no role; a role can be assigned afterwards by the superuser or an Admin member.
* Depending on its role, a user can have different access to the API ressources.
* Once created, a user can modify its password if necessary at the following endpoint  (make sure the local server is running): [http://localhost:8000/api/v1/change_password/](http://localhost:8000/api/v1/change_password/)
* A user can modify its personnal data (username, mail, location) but not its role.
* The role of a user can be modified by users with superior access rights: the superuser can change the role of an Admin member, and an Admin member can change the role of a Client.
* The personnal data of a user can be modified only by this user.
## Cars
* A car can be created by the superuser for any user.
* A car can be created by an Admin member for a client or for himself/herself.
* A car can be created by a client only for himself/herself.
* The superuser and the Admin members can access all cars or a specific car.
* A client can only have access to his/her car(s).
* The superuser can edit (update, delete) any car.
* An Admin member can edit (update, delete) any car for a Client or for themselves.
* A Client can edit (update, delete) only his/her car.
## Brands
* A Car brand can be created or edited (updated, deleted) only by the superuser or by Admin members. 
* All the users can see all brands or a specific brand.
## Models
* A Car model can be created or edited (updated, deleted) only by the superuser or by Admin members. 
* All the users can access all models or a specific model.

# Installation  

This locally-executable API can be installed and executed from using the following steps.
1.	Clone this repository using `https://github.com/Alexandremerancienne/CarsAPI.git` (you can also download the code [as a zip file](https://github.com/Alexandremerancienne/CarsAPI/archive/refs/heads/main.zip)).
2.	Move to the project root folder.
3.	Create a virtual environment (venv).
4.	Activate your venv.
5.	Install project dependencies listed in requirements.txt file : `pip install -r requirements.txt`.
8.	Migrate the data: `python manage.py migrate`.
6.	Create a superuser: `python manage.py createsuperuser`.
7.	You can consume the API with the newly created superuser, or with another user created after registration at the following endpoint: [http://localhost:8000/api/v1/register/](http://localhost:8000/api/v1/register/)
9.	Run the server: `python manage.py runserver`.  

When the server is running after step 9 of the procedure, the API can be requested after login from the endpoint [http://localhost:8000/api/v1/login/](http://localhost:8000/api/v1/login/).

# Usage and detailed endpoint documentation

One you have launched the server and opened a session, you can read the documentation through the browseable documentation interface of the API by visiting the following endpoints: 
* API users: [http://localhost:8000/api/v1/users/](http://localhost:8000/api/v1/users/)
* API cars: [http://localhost:8000/api/v1/cars/](http://localhost:8000/api/v1/cars/)
* API brands: [http://localhost:8000/api/v1/brands/](http://localhost:8000/api/v1/brands/)
* API models: [http://localhost:8000/api/v1/models/](http://localhost:8000/api/v1/models/)

All these endpoints support HTTP requests using GET, POST, PUT and DELETE methods:

# Filters
You can apply filters to search an instance of any data available in the API.
## Search and filter cars
You can search and filter cars with the following endpoint: http://localhost:8000/api/v1/cars/. The filters available are:
* `brand=<string>` to get cars filtered by brand name. The search does an exact match of the brand name.
* `brand_contains=<string>` to search cars whose brand contains the search term. 
* `model=<string>` to get cars filtered by model name. The search does an exact match of the model name.
* `model_contains=<string>` to search cars whose model contains the search term.
* `sort_by=<string>` to sort cars according to an attribute of the UserCar Model (car_brand, car_model, odo...) 
* `odo_gte=<integer>` to sort cars whose odo (odometer) is greater than the search value. 
* `odo_lte=<integer>` to sort cars whose odo (odometer) is lower than the search value. 

## Search and filter brands
You can search and filter brands with the following endpoint: http://localhost:8000/api/v1/brands/. The filters available are:
* `name=<string>` to get brands filtered by name. The search does an exact match of the name.
* `name_contains=<string>` to search brands whose name contains the search term. 

## Search and filter models
You can search and filter models with the following endpoint: http://localhost:8000/api/v1/models/. The filters available are:
* `name=<string>` to get models filtered by name. The search does an exact match of the name.
* `name_contains=<string>` to search models whose name contains the search term. 

# Endpoints test
* Endpoints can be tested with tools such as Postman or cURL.

# Documentation (Swagger/Redoc)
* The documentation of the API is available at the following endpoints (make sure the local server is running):
* Swagger: [http://localhost:8000/swagger](http://localhost:8000/swagger)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
