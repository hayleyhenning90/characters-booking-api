from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Booking Checker API is live!"

@app.route("/check_availability", methods=["GET"])
def check_availability():
    from urllib import request as urlrequest
    import json

    # Your public Google Apps Script JSON URL here
    SHEET_URL = "https://script.google.com/macros/s/AKfycbwiA2OCL9AdmpYciODtRUqxL9iPfMPV6jWd7_1v_1k7RQAvMKoBQFVPk4RcOODcBoiU/exec"

    character = request.args.get("character")
    location = request.args.get("location")
    date = request.args.get("date")
    time_str = request.args.get("time")

    res = urlrequest.urlopen(SHEET_URL)
    bookings = json.loads(res.read().decode())

    for booking in bookings:
        if (
            booking.get("Character", "").lower() == character.lower()
            and booking.get("Location", "").lower() == location.lower()
            and booking.get("Date", "").strip() == date
            and booking.get("Time from Title", "").strip() == time_str
        ):
            return jsonify({"available": False, "message": f"{character} is already booked at {time_str} on {date} in {location}."})

    return jsonify({"available": True, "message": f"{character} appears to be available at {time_str} on {date} in {location}."})
