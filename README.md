# Flask Fullstack Website
A fullstack website coded in python/flask that interacts with postgreSQL database using psycopg2.

## Functionalities

## Install
<br>
For this to work locally, you need to clone the repository and run the following command:

<br>

```
pip install psycopg2 dotenv flask flask-login bcrypt python-dotenv
```

You also need to have PostgreSQL installed and working on your machine. 

All of the database's information is stored in a .env file inside /backend/ folder and dynamically retrieved by code.

The .env file's interior should look like this:

```
host = ""
dbname = ""
user = ""
password = ""
port = ""
key = ""
```