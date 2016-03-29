#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import pandas as pd
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#

DATABASEURI = "postgresql://zj2195:UMEPTS@w4111db.eastus.cloudapp.azure.com/zj2195"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)
conn = engine.connect()
#result = conn.execute("SELECT * from Car")
#for row in result:
 # print row[0]

#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
#
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
#
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
#
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/rent')
def rent():
  cursor = g.conn.execute("SELECT Client.Username,Car.Model, Car.Type, Issue.IssueDate, Issue.ReturnDate FROM CarCopy cp, Car, Client, Issue WHERE Client.Username = Issue.Username AND Issue.VIN = cp.VIN AND  Car.VIN = cp.VIN ")
  cost = []
  for result in cursor:

   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("rent.html",**context)

@app.route('/choose')
def choose():
  cursor = g.conn.execute("SELECT * from car")
  cost = []
  for result in cursor:

   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("choose.html",**context)

@app.route('/info', methods=['POST','GET'])
def info():
  username = request.args.get('username')
  email = request.form['Email']
  g.conn.execute("UPDATE Client SET Email = '{0}' WHERE username = '{1}'".format(str(email),str(username)))
  return render_template("index.html")

@app.route('/hist', methods=['POST','GET'])
def hist():
  username = request.form['username']
  cursor = g.conn.execute("SELECT Car.Model,Car.Type,Issue.IssueDate,Issue.ReturnDate FROM Client,Issue,Car, CarCopy where Client.username = '{0}' and Client.username = Issue.username and Issue.VIN = CarCopy.VIN and Car.VIN = CarCopy.VIN" .format(str(username)))
  cost = []
  #models = []

  for result in cursor:
   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("hist.html",**context)

@app.route('/cartype')
def cartype():
  cursor = g.conn.execute("SELECT car.type, car.Model FROM car")
  cost = []
  for result in cursor:

   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("cartype.html",**context)

@app.route('/avacar')
def avacar():
  cursor = g.conn.execute("SELECT car.Vin, car.Model FROM car")
  cost = []
  for result in cursor:

   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("cartype.html",**context)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/adcar')
def adcar():
  cursor = g.conn.execute("SELECT * FROM Car")
  cost = []
  #models = []
  you = []
  for result in cursor:
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()


  cursor = g.conn.execute("SELECT Car.Model, CarCopy.Vin, CarCopy.CopyID FROM CarCopy,Car where car.vin = CarCopy.vin")
  #models = []
  you = []
  for result in cursor:
    you.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost, model = you)
  return render_template("adcar.html",**context)
@app.route('/aduser')
def aduser():
  cursor = g.conn.execute("SELECT * FROM Client")
  cost = []
  #models = []
  you = []
  for result in cursor:
   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("aduser.html",**context)

@app.route('/adstaff')
def adstaff():
  cursor = g.conn.execute("SELECT * FROM users")
  cost = []
  #models = []
  you = []
  for result in cursor:
   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("adstaff.html",**context)

@app.route('/addcopy', methods=['POST'])
def addcopy():
  VIN = request.form['VIN']
  CopyID = request.form['CopyID']
  IsChecked = request.form['IsChecked']
  IsHold = request.form['IsHold']
  IsRepaired = request.form['IsRepaired']

  g.conn.execute('INSERT INTO CarCopy VALUES (%s,%s,%s,%s,%s)', (VIN,CopyID,IsChecked,IsHold,IsRepaired))
  return redirect('/index')

@app.route('/addcar', methods=['POST'])
def addcar():
  Cost = request.form['Cost']
  Model = request.form['Model']
  VIN = request.form['VIN']
  Type = request.form['Type']
  SeatNo = request.form['SeatNo']
  g.conn.execute('INSERT INTO Car VALUES (%s,%s,%s,%s,%s)', (Cost,Model,VIN,Type,SeatNo))
  return redirect('/adcar')

@app.route('/select',methods = ['POST','GET'])
def select():
  username = request.form['username']
  VIN = request.form['VIN']
  IssueDate = request.form['IssueDate']
  ReturnDate = request.form['ReturnDate']
  NumExten = request.form['NumExten']
  ExtenDate = request.form['ExtenDate']

  g.conn.execute('INSERT INTO Issue VALUES (%s,%s,%s,%s,%s,%s,%s)', (username,VIN,12,ExtenDate,IssueDate,ReturnDate,NumExten))
  return render_template("index.html")

@app.route('/adage',methods = ['POST'])
def adage():
  age = request.form['age']
  cursor = g.conn.execute("SELECT * FROM Client where Client.age > " + age)
  cost = []
  #models = []
  you = []
  for result in cursor:
   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  context = dict(data = cost)
  return render_template("adage.html",**context)


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/client', methods = ['GET'])
def client():
  return render_template("client.html")
@app.route('/admin',methods = ['GET'])
def admin():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  # DEBUG: this is debugging code to see what request looks like
  print request.args
  #
  # example of a database query
  #
  #cursor = g.conn.execute("SELECT cost FROM Car")
  #names = []
  #for result in cursor:
  #  names.append(result['cost'])  # can also be accessed using result[0]
    #names.append(result['cost'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("admin.html")
  #return render_template("index.html")
#
# This is an example of a different path.  You can see it at
#
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (%s,%s)', (id,name))
  return redirect('/')

@app.route('/Back')
def Back():
  return redirect('/')

@app.route('/log')
def log():
  return render_template("clogin.html")

@app.route('/clogin', methods =['POST'])
def clogin():
  cursor = g.conn.execute("Select username, password From Users")
  user_info={}
  for result in cursor:
    user_info[result['username']] = result['password']
  cursor.close()

  username = request.form['username']
  password = request.form['password']

  for i in user_info.keys():
    if i == str(username) and user_info[i] == str(password):
      print "Welcome %s" %username
      weburl ='/mainpage?username=%s' %username
      return redirect(weburl)
  return redirect('/')

@app.route('/mainpage', methods =['POST','GET'])
def mainpage():
  username = request.args.get('username')
  #print username, "is in this page"
  #context = dict(data = username)
  #dict = {'username': username}
  cursor = g.conn.execute("SELECT * FROM Client where Client.username = '{0}'" .format(str(username)))
  cost = []
  #models = []
  you = []
  for result in cursor:
   # for x in result:
    #  you.append(str(x))
    #  print you
    cost.append(result)
    #models.append(result['model'])  # can also be accessed using result[0]
  cursor.close()
  #print cost
  #context = dict(data = cost)
  dict = {'cost': cost , 'username': username}
  return render_template("client.html" , dict = dict)

#@app.route('/mainpage' , methods =['POST','GET'])
#def mainpage():
#  username = request.args.get(username)
#  print username, "is in this page"
#  context = dict(data = username)
# return render_template("client.html")


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=true, threaded=threaded)


  run()

