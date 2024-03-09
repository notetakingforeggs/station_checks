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

# map route
@app.route("/")
def map_index():
    
    # call map function to generate map
    m = map()     
    
    # get the root of the map and render into a html string
    m.get_root().width = "100%"
    m.get_root().height = "500px"
    iframe = m.get_root()._repr_html_()    

    # connect to db and find most recent last checked date
    conn = sqlite3.connect("../whatsapp_scraper/stations.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(timestamp) AS stations_last_checked FROM stations;" )
    result = cursor.fetchone()
    stations_last_checked = result[0]

    # and time


    # return the map template with the map            
    return render_template("map_template.html", iframe=iframe, stations_last_checked=stations_last_checked)
    