import re
import bcrypt

def validateRegInfo(email, password, username):

    emailRe = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    passwordRe = r'([A-Za-z0-9!@#$&~()\\-`.+,/\"}{]){12,64}'
    usernameRe = r'([A-Za-z0-9]){4,12}'

    if (re.fullmatch(emailRe, email)):
        emailValid = True
    else:
        emailValid = False
    
    if (re.fullmatch(passwordRe, password)):
        passwordValid = True
    else:
        passwordValid = False
    
    if(re.fullmatch(usernameRe, username)):
        usernameValid = True
    else:
        usernameValid = False

    return emailValid, passwordValid, usernameValid

def encryptPassword(password):
    encodedPassword = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=15)
    hashedPassword = bcrypt.hashpw(encodedPassword, salt)
    stringPassword = hashedPassword.decode("utf-8") 
    return stringPassword

def comparePassword(inputPassword, databasePassword):
    encodedInput = inputPassword.encode("utf-8")
    encodedDatabase = databasePassword.encode("utf-8")
    return bcrypt.checkpw(encodedInput, encodedDatabase)