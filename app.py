from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
# import yaml
# import MySQLdb.cursors
# import re
# import logging
# from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# configure DB
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'webforum'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    message = 'Wrong details'
    if request.method == 'POST':
        userInfo = request.formpyth
        email = userInfo['email']
        password = userInfo['password']

        if email == 'test2@mail.com' and password == '123456':
            return redirect('/blog')
        else:
            return redirect('/register')

    return render_template('index.html')


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


@app.route('/blog')
def blog():
    return render_template('blog.html')


if __name__ == '__main__':
    app.run(debug=True)
