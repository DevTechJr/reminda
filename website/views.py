from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Sighting, People
from . import db
import json
import datetime

views = Blueprint('views', __name__)

@views.route('/getSightings', methods=['GET'])
def get_sightings():
    sightings = Sighting.query.all()  # Replace with your actual data retrieval method
    timestamps = [sighting.time.strftime("%Y-%m-%d %H:%M:%S") for sighting in sightings]  # Format as needed
    return jsonify(timestamps)

@views.route('/getAll', methods=['GET'])
def get_all():
    sightings = Sighting.query.all()  # Replace with your actual data retrieval method
    sightings = [{"name": sighting.name, "location": sighting.location, "time": sighting.time.strftime("%Y-%m-%d %H:%M:%S")} for sighting in sightings]
    print("SIGHTINGS: ", sightings)
    return jsonify(sightings)

@views.route('/getNames', methods=['GET'])
def get_names():
    sightings = Sighting.query.all()  # Replace with your actual data retrieval method
    names = []
    for sighting in sightings:
        names.append(sighting.name)
    return jsonify(names)


@views.route('/getLocations', methods=['GET'])
def get_locations():

    sightings = Sighting.query.all()
    locations = []
    for sighting in sightings:
        locations.append(sighting.location)

    print("LOCATIONS: ", locations)
    return jsonify(locations)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    sightingData = []
    sightings = Sighting.query.all()
    timestamps = []
    for sighting in sightings:
        timestamps.append(sighting.time)
        sightingData.append({"name": sighting.name, "location": sighting.location, "time": sighting.time})

    people = People.query.all()
    peopleData = []

    # Create a dictionary to store the last seen timestamp for each person
    last_seen = {}
    for sighting in sightings:
        if sighting.name not in last_seen:
            last_seen[sighting.name] = sighting.time
        else:
            # Update the last seen timestamp if the current one is more recent
            if sighting.time > last_seen[sighting.name]:
                last_seen[sighting.name] = sighting.time

    # Construct peopleData with last_seen_at
    for person in people:
        peopleData.append({
            "name": person.name,
            "picture": person.picture,
            "relation": person.relation,
            "summary": person.summary,
            "specialMemory": person.specialMemory,
            "last_seen_at": last_seen.get(person.name, None)  # Get the last seen timestamp or None if not found
        })
    
    return render_template("home.html", user=current_user, sightings=sightings, timestamps=timestamps, sightingData=sightingData, peopleData=peopleData)

@views.route('/addSighting', methods=['POST', "GET"])
def addSighting():
    userName = request.args.get("name")
    relation = request.args.get("relation")
    userLocation = request.args.get("location")

    print("Name: ", userName)

    new_sighting = Sighting(name=userName, location=userLocation)
    db.session.add(new_sighting)
    db.session.commit()

    return jsonify({"message": "Sighting added successfully!"})




