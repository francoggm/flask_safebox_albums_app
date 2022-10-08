<h1> A webapp how locks albums with pins, to maintain all yours photos safe. </h1>

<h3>The project uses the following technologies</h3>
  > Python (Flask and Flask modules) <br>
  > MySQL <br>
  > JavaScript Vanilla <br>
  > Bootstrap 5 <br>

<h3> Project </h3>
The auth.py file is in charge of creating, validating and saving new or existing users in the database.
The views.py file takes care of the remaining routes of the project, routes to create and delete albums, upload and delete images, change user information and access the default templates for the same.
<br>
To be able to run the database, you must already have a database in MySQL called users, or if you already have one, modify line 7 of the __init__.py file: <br>
> app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/users' < <br>
and change 'users' to your database name.
<br>
 -> If you get any other MySQL username/password error, try setting the URI correctly for your MySQL server
<br>
The dependencies and their versions to run the project are in the requirements.txt file, preferably install exactly as described in this file. After that, just run the main.py file to open the project on a localhost port, if there are any route errors during execution, try the route number in the 'port' parameter of the run method (main.py file, line 4).
