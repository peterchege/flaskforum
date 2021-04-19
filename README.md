# flaskforum
This is a forum built using Python and Flask, a microweb framework

# Tools Used
Python 3.9
Flask
Virtualenv
Flask-mysqldb

First of all, we need to create a Virtual environment using a tool known as virtualenv because it is best practice to do so.
Virtualenv isolates your Python set-up on a per-project basis. Make sure to install the Virtualenv tool by doing the following:

```bash
pip install virtualenv
```

# Setting up a virtual environment
Make sure to pick a virtual environment name that is in lower case and has no special characters or spaces
```bash
virtualenv venv
```
Also ensure that the virtual environment is set up in the working directory of the project

# Working with the virutal environment
To activate it:
```bash
source ./venv/scripts/activate
```

You will know that you have virtualenv started when you see that the prompt in your console is prefixed with
(venv)

Use pip, a package management system that comes with python on installation, to install the tools for the project

```bash
pip install flask
pip install virtualenv
pip install flask-mysqldb
```
Alternatively, the packages are listed in the requirements.txt file and can be installed using
```bash
pip install requirements.txt
```

# Running the program
```bash
python app.py
```

