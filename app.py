from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS  # Import CORS to enable cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from different origins

# Serve the map page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive location data
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    print("Received data:", data)

    # Extracting coordinates from JSON data
    latitude1 = data.get('latitude1')
    longitude1 = data.get('longitude1')
    latitude2 = data.get('latitude2')
    longitude2 = data.get('longitude2')
    
    # Save to SQLite database
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitudeStart REAL,
            longitudeStart REAL,
            latitudeEnd REAL,
            longitudeEnd REAL
        )
    ''')
    cursor.execute('''
        INSERT INTO locations (latitudeStart, longitudeStart, latitudeEnd, longitudeEnd)
        VALUES (?, ?, ?, ?)
    ''', (latitude1, longitude1, latitude2, longitude2))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({
        'status': 'success',
        'message': 'Coordinates saved successfully',
        'data': {
            'latitude1': latitude1,
            'longitude1': longitude1,
            'latitude2': latitude2,
            'longitude2': longitude2
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
