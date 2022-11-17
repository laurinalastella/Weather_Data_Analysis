# package for building webpage
from flask import Flask, render_template, redirect, url_for

# our datacleaning functions
import Laurina_Alice_GetCleanData_sandbox3 as gcda

# webpage code
appBob = Flask(__name__)

@appBob.route('/')
def welcome():
    return render_template("front.html")

@appBob.route("/api/v1.0/history_loc/<country>/<location>/<start_date_iso>/<end_date_iso>")
def loc_stats(country, location, start_date_iso, end_date_iso):
    return gcda.get_adjective_stats_loc(country, location, start_date_iso, end_date_iso)



# stuff below is old/broken/irrelevant, or new/broken/unfininshed


@appBob.route("/api/v1.0/history_latlong/<lattitude>/<longitude>/<start_date_iso>/<end_date_iso>/<years>")
def latlong_stats(lattitude, longitude, start_date_iso, end_date_iso, years=20):
    lattitude = float(lattitude)
    longitude = float(longitude)
    years = int(years)
    return gcda.get_adjective_stats(lattitude, longitude, start_date_iso, end_date_iso, years)

@appBob.route("/api/v1.0/prettyy/<lattitude>/<longitude>/<start_date_iso>/<end_date_iso>/<years>")
def pretty_stats(lattitude, longitude, start_date_iso, end_date_iso, years=20):
    lattitude = float(lattitude)
    longitude = float(longitude)
    years = int(years)
    return gcda.get_adjective_stats(lattitude, longitude, start_date_iso, end_date_iso, years)
    # weather_dict = gcda.get_adjective_stats(lattitude, longitude, start_date_iso, end_date_iso, years)
    # weather_dict['start'] = start_date_iso
    # weather_dict['end'] = end_date_iso
    # weather_dict['years'] = years
    # return render_template("pretty.html", weather_data = weather_dict)




