from flask import Flask, flash, redirect, render_template, request, session, g 
from flask_session import Session

from map import map

import sqlite3


# Configure application
app = Flask(__name__)

# am i using session? dont think so...
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['STATIC_FOLDER'] = 'static'
Session(app) 

# connect to stations database
conn = sqlite3.connect("stations.db")
cursor = conn.cursor()
# map route
@app.route("/")
def map_index():
    
    # call map function to generate map
    m = map()     
    
    # get the root of the map and render into a html string
    m.get_root().width = "100%"
    m.get_root().height = "500px"
    iframe = m.get_root()._repr_html_()    

    # return the map template with the map            
    return render_template("map_template.html", iframe=iframe)
    