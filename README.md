# Example code for REST API 2 presentation at [IEPUG](https://www.meetup.com/iepython/events/286366168/) on 7/19/2022
This is a follow-up for the [Intro to REST APIs](https://www.meetup.com/iepython/events/284263024/) presentation the month before. Example code and slides for that presentation can be found [here](https://github.com/IEPUG/2020_02_REST-API).

### Basic Flask routing
- _rest_server1.py_: - Basic Flask setup with Flask route decorators

### Using Flask-RESTful routing
- _rest_server2.py_: - Flask setup with Flask-RESTful classes

### Using Flask Blueprints
- _rest_server3.py_: - Moved routes to separate file with Flask Blueprints
- _db_routes3.py_: - GET routes for database access

### Adding additional HTTP request methods
- _rest_server4.py_: - Moved routes to separate file with Flask Blueprints
- _db_routes4.py_: - GET, POST, PUT, and DELETE routes for database access

### Adding Flask-Login (Final form)
- _rest_server.py_: - Moved routes to separate file with Flask Blueprints
- _db_routes.py_: - GET, POST, PUT, and DELETE routes for database access
- _admin_routes.py_: Admin routes for session control (Login/Logout)

### Additional Files
- _db_utils.py_: Convenience funcitons for working with the sqlite database
- _rest_test.http_: HTTP requests for testing REST API in PyCharm

