import os
import sys
import shutil

templates_folder = "/templates"
static_folder = "/static"

# create directory for application
def create_dir(app_name):
    os.mkdir(app_name)

# create app.py in directory 'app_name'
def create_app(app_name, addDebug):
    appPy = open(app_name + "/app.py", "w+")
    if (addDebug):
        print("-debug mode on")
        linePython = "from flask import Flask, render_template\n" + "app = Flask(__name__)\n\n" + "@app.route('/')\n" + "def hello():\n" + "\treturn render_template('index.html')\n\n" + "if __name__ == '__main__':\n" + "\tapp.run(debug=True, host='0.0.0.0')\n"
    else:
        linePython = "from flask import Flask, render_template\n" + "app = Flask(__name__)\n\n" + "@app.route('/')\n" + "def hello():\n" + "\treturn render_template('index.html')\n\n" + "if __name__ == '__main__':\n" + "\tapp.run(host='0.0.0.0')\n"
    appPy.writelines([linePython])
    appPy.close()

# create templates folder in directory
def create_templates_folder(app_name, addStyleScript):
    os.makedirs(app_name + templates_folder)
    if (addStyleScript):
        lineHtml ="""
<!DOCTYPE html>
<html>
  <head>
    <title>Hello World</title>
    <link rel='stylesheet' href='/static/stylesheet/style.css'>
  </head>
  <body>
    <h1>Hello World!!</h1>
    <script src='/static/js/app.js'></script>
  </body>
</html>
"""
    else:
        lineHtml = """
<!DOCTYPE html>
<html>
  <head>
    <title>Hello World</title>
  </head>
  <body>
    <h1>Hello World!!</h1>
  </body>
</html>
"""
    indexHtml = open(app_name + templates_folder + "/index.html", "w+")
    indexHtml.writelines([lineHtml])
    indexHtml.close()

# create static folder in directory
def create_static_folder(app_name):
    # This is where stylesheets goes
    print("-css & js mode on")
    os.makedirs(app_name + static_folder + "/stylesheet")
    cssFile = open(app_name + static_folder + "/stylesheet" + "/style.css", "w+")
    cssFile.close()

    # This is where javascript goes
    os.makedirs(app_name + static_folder + "/js")
    jsFile = open(app_name + static_folder + "/js" + "/app.js", "w+")
    jsFile.close()

# manage docker contents in app folder
def create_dockerfile(app_name):
    # move folders in app folder
    os.makedirs(app_name + "/app")
    files = os.listdir(app_name)
    for f in files:
        if f != 'app':
            shutil.move(app_name + '/' + f, app_name + "/app")

    # create requirements.txt
    requirements_txt = open(app_name + "/app/requirements.txt", "w+")
    linePython = "flask\n"
    requirements_txt.writelines([linePython])
    requirements_txt.close()

    # create Dockerfile
    dockerfile_txt = open(app_name + "/app/Dockerfile", "w+")
    linePython = "FROM python:3.7-alpine \nWORKDIR /app \nCOPY . /app \nRUN pip3 install -r requirements.txt \nENTRYPOINT [\"python3\"] \nCMD [\"app.py\"]"
    dockerfile_txt.writelines([linePython])
    dockerfile_txt.close()

    # create docker-compose.yml
    dockercompose_yml = open(app_name + "/docker-compose.yml", "w+")
    linePython = "version: '3' \nservices: \n  web: \n    build: app \n    ports: \n      - '5000:5000'"
    dockercompose_yml.writelines([linePython])
    dockercompose_yml.close()

    print("-dockerfile generated")
    print('  --> cd %s' % app_name)
    print('  --> \"docker-compose up -d\" to start app')