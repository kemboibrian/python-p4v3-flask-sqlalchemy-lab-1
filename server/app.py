# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    try:
        # Query the database for earthquakes with magnitude greater than or equal to the given value
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

        # Count the number of earthquakes found
        count = len(earthquakes)

        # Prepare the response JSON
        response = {
            "count": count,
            "quakes": []
        }

        # Format each earthquake data and add to the response
        for earthquake in earthquakes:
            quake_data = {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
            }
            response["quakes"].append(quake_data)

        # Return the JSON response
        return jsonify(response), 200
    
    except Exception as e:
        # Handle exceptions or database errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
