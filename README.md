# Strava Club Leaderboard

This application creates an interactive leaderboard for a Strava club, displaying total activities and stats for each member. It uses the Strava API to fetch club activities and presents them in a responsive, sortable web interface. The application consists of a Flask backend and a React frontend.

## Features

- 🔐 OAuth 2.0 authentication with Strava
- 🔄 Fetches and caches club activities
- 📊 Calculates total distance, moving time, elapsed time, elevation gain, and average mileage per activity for each athlete
- 🏆 Displays a sortable and searchable leaderboard based on various metrics
- 📱 Responsive web design with modern UI
- 🔍 Search functionality for quick athlete lookup
- 📄 Pagination for easy navigation through large datasets
- 📊 Export leaderboard data to CSV

## Prerequisites

- Python 3.7+
- Node.js 14+ and npm
- A Strava API application (for Client ID and Client Secret)
- Strava Club ID

## Installation

### Backend (Flask)

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

### Frontend (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the required npm packages:
   ```bash
   npm install
   ```

   This will install the following main dependencies:
   - react
   - react-dom
   - react-scripts
   - axios
   - react-table

   For a full list of dependencies and their versions, see the `package.json` file in the `frontend` directory.

3. Start the development server:
   ```bash
   npm start
   ```

   This will run the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Usage

1. Start the Flask backend:
   ```bash
   cd backend
   python leaderboard.py
   ```

2. In a separate terminal, start the React frontend:
   ```bash
   cd frontend
   npm start
   ```

3. Open a web browser and navigate to `http://localhost:3000`

4. If not already authenticated, you'll be redirected to Strava for authorization

5. Once authenticated, you'll see the interactive leaderboard for your Strava club

6. Click the "Export to CSV" button to download the leaderboard data as a CSV file

## Customization

- The leaderboard's appearance can be customized by modifying the CSS in `frontend/src/App.css`
- Adjust the caching duration by changing the `TTLCache` parameters in `leaderboard.py`
- Modify the React components in `frontend/src/App.js` to change table behavior or add new features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Strava API](https://developers.strava.com/) for providing access to club data
- [Flask](https://flask.palletsprojects.com/) for the backend web framework
- [React](https://reactjs.org/) for the frontend user interface
- [react-table](https://react-table.tanstack.com/) for the interactive table functionality
- [Requests](https://docs.python-requests.org/) for handling HTTP requests
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables

---

Made with ❤️ by icepuente