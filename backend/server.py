import psycopg2
import auth
import database
from flask import Flask, request, render_template, redirect, session
from dotenv import load_dotenv
import bcrypt
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


load_dotenv()
portEnv = os.getenv("port")

## flask constructor
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.debug = True
log = LoginManager()
log.init_app(app)
app.secret_key = os.getenv("key")

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def get(userId):
        connection = database.getDatabaseConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = (%s)", (userId))
        userData = cursor.fetchone()
        cursor.close()
        connection.close()
        if userData:
            return User(userData[0], userData[1], userData[2])
        return None

@log.user_loader
def load_user(userId):
    return User.get(userId)

## associate url with function
@app.route('/')
def index():
        return render_template('index.html')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect("/", 301)
    else:
        return render_template('login.html')

@app.route('/login-form', methods =["GET","POST"])
def getLogInfo():
    if request.method == "POST":
        email = request.form.get("email")
        inputPassword = request.form.get("password")
        connection = database.getDatabaseConnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT id, username, email FROM users WHERE email = (%s)""", (email,))
        user_data = cursor.fetchone()
        databasePassword = database.getPasswordDatabase(email)
        databaseUsername = database.getUsernameDatabase(email)
        if auth.comparePassword(inputPassword, databasePassword) == True:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect("/", 301)
        else:
            return "You are not logged in"
        
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/", 302)

@app.route('/register-form', methods =["GET", "POST"])
def getRegInfo():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        emailValid, passwordValid, usernameValid = auth.validateRegInfo(email, password, username)
        if emailValid == True and passwordValid == True and usernameValid == True:
            hashedPassword = auth.encryptPassword(password)
            database.createTablesUsers()
            database.insertTableUsers(username, hashedPassword, email)
            return redirect("/", code = 302)
        else:
            return "Registration failed"

if __name__ == '__main__':
    app.run()
