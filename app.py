# Import modules

import datetime as dt
import numpy as np
import pandas as pd

# Import dependecies for SQLAlchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependency for Flask

from flask import Flask, jsonify

# Set up database engine for flask application

engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database in classes

Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from python to database

session = Session(engine)

# Define app for flask application

app = Flask(__name__)

# Define welcome route

@app.route("/")

# Create function to add routing information

def welcome():
    return (
        '''
    Welcome to the Climate Analysis API!

    Available Routes:
    
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    '''
    )

# percipitation data for the last year, write a query to get date and percipitation for previous year.
# also create a dictionary with the date as key and percipitation as value and then jsonify it.

@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    
    return jsonify (precip)


# stations route

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# temperature observations for the previous year
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# report route to indicate minimum, maximum and average temperatures

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
