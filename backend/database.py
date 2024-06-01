from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
hostEnv = os.getenv("host")
dbnameEnv = os.getenv("dbname")
userEnv = os.getenv("user")
passwordEnv = os.getenv("password")

def getDatabaseConnection():
    connection = psycopg2.connect(host=hostEnv, dbname=dbnameEnv, user=userEnv, password=passwordEnv)
    return connection

def createTablesUsers():
    """Create the table users if it does not already exists."""
    connection = getDatabaseConnection()
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username text,
            password Varchar(255),
            email Varchar(255)
                );
                   """)
    connection.commit()
    connection.close()

def insertTableUsers(username, hashPassword, email):
    """Insert username, hash of the password and email on the table users."""
    connection = getDatabaseConnection()
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s);""", 
    (username, hashPassword, email))
    connection.commit()
    connection.close()

def getPasswordDatabase(email):
    """Retrieves the password from the database based on the e-mail informed.\n\n Requires the user e-mail (string) and returns the password (string)."""

    connection = getDatabaseConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT password FROM users WHERE email = (%s);""", 
    (email,))

    password = cursor.fetchone()

    connection.commit()
    connection.close()

    return str(password[0])


def getUsernameDatabase(email):

    """Retrieves the password from the database based on the e-mail informed.\n\n Requires the user e-mail (string) and returns the password (string)."""

    connection = getDatabaseConnection()
    cursor = connection.cursor()

    cursor.execute("""SELECT username FROM users WHERE email = (%s);""", 
    (email,))

    username = cursor.fetchone()

    connection.commit()
    connection.close()

    return str(username[0])