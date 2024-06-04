from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def connect_database():

    try:
        connection = psycopg2.connect(host=os.getenv("host"), 
                                      dbname=os.getenv("dbname"), 
                                      user=os.getenv("user"), 
                                      password=os.getenv("password"),
                                      port=os.getenv("port"))
        return connection

    except Exception as err:
        print(err)

def create_table_users():
    """Create the table users if it does not already exists."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username text, password Varchar(255), email Varchar(255), imagepath Varchar(255));""")
        con.commit()
        con.close()
        cur.close()
    except Exception as err:
        print(err)

def insert_user(username, hash_password, email):
    """Insert new user row (id, username, password hash, email) in the table users."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s);""", 
    (username, hash_password, email))
        con.commit()
        con.close()
        cur.close()
    except Exception as err:
        print(err)

def select_password(email):
    """Selects the user's password from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT password FROM users WHERE email = (%s);""", (email,))
        password = cur.fetchone()
        con.close()
        cur.close()

        return password[0]
    except Exception as err:
        print(err)

def select_username(email):
    """Selects the user's username from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT username FROM users WHERE email = %s;""", (email,))
        username = cur.fetchone()
        con.close()
        cur.close()

        return username[0]

    except Exception as err:
        print(err)

def select_data(email):
    """Selects the user's id, username, email and password hash from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute(
        """SELECT id, username, email, password FROM users WHERE email=(%s);""", (email,))
        data = cur.fetchone()
        con.close()
        cur.close()
        id = data[0]
        username = data[1]
        email = data[2]
        password =  data[3]
        return id, username, email, password
    except Exception as err:
        print(err) 

def update_username(id, username):
    """Updates the user's username in the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET username = %s WHERE id = %s;""", (username, id))
        con.commit()

        con.close()
        cur.close()
    except Exception as err:
        print(err)

def update_password(id, password):
    """Updates the user's password hash inside the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET password = %s WHERE id = %s;""", (password, id))
        con.commit()
        con.close()
        cur.close()
    except Exception as err:
        print(err)