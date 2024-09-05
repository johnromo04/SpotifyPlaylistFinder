

# Spotify Playlist Finder

A simple Flask app to authenticate with Spotify, view playlists, and find playlists containing a specific track by an artist.
For those with many playlists

## Features

- **Spotify Authentication**
- **View Playlists**
- **Search for a Track in Playlists**

## Setup

### Prerequisites

- Python 3.x
- Spotify Developer Account (for Client ID and Secret)

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/spotify-playlist-finder.git
   cd spotify-playlist-finder
   
2. Install Dependencies

    ```bash
    pip install -r requirements.txt
    
3. Create secret.py with Spotify credentials which can be found here at [Spotify Developer](https://developer.spotify.com):
    
    
    ```bash
    SPOTIPY_CLIENT_ID = 'your_client_id'
    SPOTIPY_CLIENT_SECRET = 'your_client_secret'
    SPOTIPY_REDIRECT_URI = 'your_redirect_uri'
    
4. Run the app:
    
    ```bash
    python app.py
    
## Usage

1. Navigate to http://localhost:5432/ for Spotify login.

2. Go to /show_playlists to view your playlists.

3. Search for a track in playlists by visiting:
    
    ```bash
    /find_playlist?track=<track_name>&artist=<artist_name>
    
## Routes
* /: Redirects to Spotify for login.
* /callback: Handles Spotify callback after login.
* /show_playlists: Displays your playlists.
* /find_playlist: Search playlists for a track by an artist.




