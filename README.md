# Strava Club Leaderboard

This Flask application creates an interactive leaderboard for a Strava club, displaying total activities and stats for each member. It uses the Strava API to fetch club activities and presents them in a responsive, sortable web interface.

## Features

- 🔐 OAuth 2.0 authentication with Strava
- 🔄 Fetches and caches club activities
- 📊 Calculates total distance, moving time, elapsed time, and elevation gain for each athlete
- 🏆 Displays a sortable leaderboard based on various metrics
- 📱 Responsive web design with modern UI
- 🔍 Search functionality for quick athlete lookup
- 📄 Pagination for easy navigation through large datasets

## Prerequisites

- Python 3.7+
- A Strava API application (for Client ID and Client Secret)
- Strava Club ID

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/icepuente/strava-club-leaderboard.git
   cd strava-club-leaderboard
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory with the following content:
   ```
   STRAVA_CLIENT_ID=your_client_id
   STRAVA_CLIENT_SECRET=your_client_secret
   STRAVA_REFRESH_TOKEN=your_refresh_token
   STRAVA_CLUB_ID=your_club_id
   STRAVA_REDIRECT_URI=http://localhost:5000/callback
   ```
   Replace the placeholders with your actual Strava API credentials and club ID.

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. If not already authenticated, you'll be redirected to Strava for authorization

4. Once authenticated, you'll see the interactive leaderboard for your Strava club

## Customization

- The leaderboard's appearance can be customized by modifying the CSS in `templates/index.html`
- Adjust the caching duration by changing the `TTLCache` parameters in `app.py`
- Modify the DataTables options in `templates/index.html` to change table behavior

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Strava API](https://developers.strava.com/) for providing access to club data
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Requests](https://docs.python-requests.org/) for handling HTTP requests
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables
- [DataTables](https://datatables.net/) for the interactive table functionality

---

Made with ❤️ by icepuente
