from flask import Flask, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required to use Flask sessions
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI = SPOTIPY_REDIRECT_URI
scope = 'playlist-read-private'

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope)

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        try:
            token_info = sp_oauth.get_access_token(code)
            session['token_info'] = token_info  # Save the token info in the session
            return redirect(url_for('show_playlists'))
        except spotipy.SpotifyException as e:
            return f'Error: {e}'
    else:
        return 'Error: Missing authorization code in callback'

@app.route('/show_playlists')
def show_playlists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('index'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Example: Get current user's playlists
    playlists = sp.current_user_playlists()
    playlist_names = [playlist['name'] for playlist in playlists['items']]
    
    return f'Playlists: {playlist_names}'

@app.route('/find_playlist')
def find_playlist():
    track_name = request.args.get('track')
    artist_name = request.args.get('artist')

    if not track_name or not artist_name:
        return 'Error: Missing track or artist parameter'

    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('index'))

    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Search for the track
        results = sp.search(q=f'track:{track_name} artist:{artist_name}', type='track')
        if not results['tracks']['items']:
            return f'No track found for {track_name} by {artist_name}'
        
        track_id = results['tracks']['items'][0]['id']
        
        # Find playlists containing the track
        playlists = sp.current_user_playlists()
        playlist_containing_track = []

        while playlists:
            for playlist in playlists['items']:
                playlist_id = playlist['id']
                playlist_tracks = sp.playlist_tracks(playlist_id)
                
                for item in playlist_tracks['items']:
                    if item and item['track'] and item['track']['id'] == track_id:
                        playlist_containing_track.append(playlist['name'])
                        break

            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

        if playlist_containing_track:
            return f'Playlists containing "{track_name}" by {artist_name}: {playlist_containing_track}'
        else:
            return f'No playlists contain the track "{track_name}" by {artist_name}'
    except spotipy.SpotifyException as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(port=5432, debug=True)
