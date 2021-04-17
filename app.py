from flask import Flask, render_template, request, redirect, jsonify,session, url_for
from flask_mysqldb import MySQL
from jinja2 import nodes
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'forum'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def login():
    """  Checks if the username and password POST requests exist (i.e. that the user submittet) """
    message = ''
    if request.method == 'POST':
        userInfo = request.form
        email = userInfo['email']
        password = userInfo['password']
        #check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        #fetch one record and returns result
        user = cursor.fetchone()

        #if user exists in users table in the DB
        if user:
            #create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            #redirect to homepage
            return render_template('forum.html')
        else:
            #A/c does not exist or email/password is incorrect
            message = 'Incorrect username/password! If you do not have an account, please register on the left'
        #show the login form with message (if any)

    return render_template('index.html', message = message)


@app.route('/register', methods=['POST', 'GET'])
def register():
    # msg if sthg goes wrong
    message=''
    #Check if 'username','password' and 'email' POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        #check if account exits using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cursor.fetchone()
        #if account exists show error and validation checks
        if user:
            message = 'User already exists'
        elif not re.match(r'[A-Za-z0-9]+', name):
            message = 'Username must only contain characters and numbers'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not name or not password or not email:
            message = 'Please fill out the form'
        else:
            #Account doesnt exists and the form data is valid, 
            # now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s,%s,%s)', (name,email,password,))
            mysql.connection.commit()
            message = 'You have successfully created an account'
    elif request.method == 'POST':
        #If form is empty...
        message = 'Please complete the Form'
    #show registration form with the message(if any)
    return render_template('index.html', message = message)


@app.route('/logout')
def logout():
    #remove session data, this logs out user
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    #Redirect to login page
    return redirect(url_for('index'))


@app.route('/forum')
#home page only accessible to loggein members
def forum():
    #check if user is logged in
    if 'loggedin' in session:
        #user is logged in and can see homepage
        return render_template('forum.html', name=session['name'])
    #user is not logged in and cant see homepage
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
