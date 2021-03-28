from flask import Flask, render_template, request, redirect, jsonify,session, url_for
from flask_mysqldb import MySQL
from jinja2 import nodes
import MySQLdb.cursors
import re


# import yaml
# import MySQLdb.cursors
# import re
# import logging
# from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# configure DB
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'forum'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
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
            return 'Logged in successfully!'
        else:
            #A/c does not exist or email/password is incorrect
            message = 'Incorrect username/password!'
        #show the login form with message (if any)
    return render_template('index.html', message = message)


# @app.route('/test', methods=['GET'])
# def test():
#     print('inside test')
#     return jsonify({'success':'yup'})

# bringing a 404 error
# not loading css
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(username, email, password) VALUES(%s,%s,%s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        # return 'Success'
    return render_template('register.html')


@app.route('/forum')
def forum():
    return render_template('forum.html')


if __name__ == '__main__':
    app.run(debug=True)
