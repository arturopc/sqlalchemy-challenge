import sqlalchemy
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index(): 
    return (f"Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > "2016-08-23")
                      .order_by(Measurement.date)
                      .all())
    precipitation = []
    for value in results:
        temp = {value.date: value.prcp, "Station": value.station}
        precipitation.append(temp)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    results = (session.query(Station.id, Station.station, Station.name)
                      .all())
    stations = []
    for value in results:
        temp = {"ID": value.id, "Station": value.station, "Name": value.name}
        stations.append(temp)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
    results = (session.query(Measurement.date, Measurement.tobs)
                      .filter(Measurement.date > "2016-08-23")
                      .order_by(Measurement.date)
                      .all())
    tobs = []
    for value in results:
        temp = {"Date": value.date, "Temperature": value.tobs}
        tobs.append(temp)
    return jsonify(tobs)

@app.route("/api/v1.0/<startDate>")
def start(startDay):
    return (session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                      .filter(Measurement.date == startDay)
                      .all())

@app.route("/api/v1.0/<startDate>/<end>")
def startEnd(startDay, endDay):
    return (session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                      .filter(Measurement.date >= startDay)
                      .filter(Measurement.date <= endDay)
                      .all())
    
if __name__ == "__main__":
    app.run()