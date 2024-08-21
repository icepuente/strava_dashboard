from datetime import datetime
from flask import Flask, redirect, request, url_for, render_template, jsonify, make_response
import requests
from cachetools import cached, TTLCache
import time
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, List, Tuple
import csv
from io import StringIO
from flask import send_file
from io import BytesIO
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credential support
app.secret_key = os.urandom(24)

@dataclass
class TokenInfo:
    access_token: str
    refresh_token: str
    expires_at: int

@dataclass
class AthleteStats:
    total_distance: float
    total_moving_time: int
    total_elapsed_time: int
    total_elevation_gain: float
    activity_count: int
    average_distance: float

# Environment variables
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')
CLUB_ID = int(os.getenv('STRAVA_CLUB_ID', '581605'))
REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI', 'http://localhost:5000/callback')

# Cache to store the activities, TTL of 3600 seconds (1 hour)
cache = TTLCache(maxsize=1, ttl=3600)
token_info = TokenInfo(access_token=None, refresh_token=REFRESH_TOKEN, expires_at=0)

@app.template_filter('seconds_to_hms')
def seconds_to_hms_filter(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

@app.route('/login')
def login():
    login_url = f'https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=auto&scope=activity:read_all,activity:write'
    return redirect(login_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed.', 400

    token_response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    ).json()

    token_info.access_token = token_response['access_token']
    token_info.refresh_token = token_response['refresh_token']
    token_info.expires_at = token_response['expires_at']

    response = make_response(redirect('http://localhost:3000'))
    response.set_cookie('authenticated', 'true', httponly=True, samesite='Lax')
    return response

def refresh_access_token():
    token_response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': token_info.refresh_token
        }
    ).json()

    token_info.access_token = token_response['access_token']
    token_info.refresh_token = token_response['refresh_token']
    token_info.expires_at = token_response['expires_at']

def get_access_token():
    current_time = int(time.time())
    if current_time >= token_info.expires_at - 600:  # Refresh if less than 10 minutes remaining
        refresh_access_token()
    return token_info.access_token

def meters_to_miles(meters: float) -> float:
    return meters * 0.000621371

def meters_to_feet(meters: float) -> float:
    return meters * 3.28084

@cached(cache)
def fetch_club_activities() -> List[Dict]:
    headers = {'Authorization': f'Bearer {get_access_token()}'}
    activities = []
    page = 1
    per_page = 200

    while True:
        url = f'https://www.strava.com/api/v3/clubs/{CLUB_ID}/activities'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        if not data:
            break

        activities.extend(data)
        page += 1

    return activities

def process_activities(activities: List[Dict]) -> List[Tuple[str, AthleteStats]]:
    leaderboard = {}
    for activity in activities:
        athlete_name = f"{activity['athlete']['firstname']} {activity['athlete']['lastname']}"
        if athlete_name not in leaderboard:
            leaderboard[athlete_name] = AthleteStats(0, 0, 0, 0, 0, 0)

        stats = leaderboard[athlete_name]
        stats.total_distance += meters_to_miles(activity['distance'])
        stats.total_moving_time += activity['moving_time']
        stats.total_elapsed_time += activity['elapsed_time']
        stats.total_elevation_gain += meters_to_feet(activity['total_elevation_gain'])
        stats.activity_count += 1
        stats.average_distance = stats.total_distance / stats.activity_count

    return sorted(leaderboard.items(), key=lambda x: x[1].total_distance, reverse=True)

@app.route('/')
def index():
    if not token_info.access_token:
        return redirect(url_for('login'))

    activities = fetch_club_activities()
    leaderboard = process_activities(activities)
    return render_template('index.html', leaderboard=leaderboard)

@app.route('/api/leaderboard')
def get_leaderboard():
    if not token_info.access_token:
        return jsonify({"error": "Not authenticated"}), 401

    activities = fetch_club_activities()
    leaderboard = process_activities(activities)
    return jsonify([
        {
            "rank": idx + 1,
            "athlete": athlete,
            "totalDistance": round(stats.total_distance, 2),
            "averageDistance": round(stats.average_distance, 2),
            "totalMovingTime": stats.total_moving_time,
            "totalElapsedTime": stats.total_elapsed_time,
            "totalElevationGain": round(stats.total_elevation_gain, 0),
            "activityCount": stats.activity_count
        }
        for idx, (athlete, stats) in enumerate(leaderboard)
    ])

@app.route('/api/export_csv')
def api_export_csv():
    activities = fetch_club_activities()
    leaderboard = process_activities(activities)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Rank', 'Athlete', 'Total Distance (miles)', 'Average Distance (miles)', 'Total Moving Time', 'Total Elapsed Time', 'Total Elevation Gain (feet)', 'Number of Activities'])

    for idx, (athlete, stats) in enumerate(leaderboard, 1):
        writer.writerow([
            idx,
            athlete,
            f"{stats.total_distance:.2f}",
            f"{stats.average_distance:.2f}",
            seconds_to_hms_filter(stats.total_moving_time),
            seconds_to_hms_filter(stats.total_elapsed_time),
            f"{stats.total_elevation_gain:.0f}",
            stats.activity_count
        ])

    # Convert to BytesIO
    output.seek(0)
    bytes_output = BytesIO()
    bytes_output.write(output.getvalue().encode('utf-8'))
    bytes_output.seek(0)

    return send_file(bytes_output,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='strava_club_leaderboard.csv')

@app.route('/api/check-auth')
def check_auth():
    if token_info.access_token:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})

if __name__ == '__main__':
    app.run(debug=True)