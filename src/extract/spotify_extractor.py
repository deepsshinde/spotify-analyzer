import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyExtractor:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-recently-played user-top-read"
        ))
    
    def get_recently_played(self, limit=50):
        """Get recently played tracks"""
        results = self.sp.current_user_recently_played(limit=limit)
        
        tracks_data = []
        for item in results['items']:
            track = item['track']
            tracks_data.append({
                'played_at': item['played_at'],
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name'],
                'album_name': track['album']['name'],
                'duration_ms': track['duration_ms']
            })
        
        return pd.DataFrame(tracks_data)
    
    def get_audio_features(self, track_ids):
        """Get audio features for tracks"""
        features = self.sp.audio_features(track_ids)
        
        features_data = []
        for f in features:
            if f:  # Sometimes returns None
                features_data.append({
                    'track_id': f['id'],
                    'danceability': f['danceability'],
                    'energy': f['energy'],
                    'tempo': f['tempo'],
                    'valence': f['valence'],  # Musical positivity
                    'acousticness': f['acousticness']
                })
        
        return pd.DataFrame(features_data)

# Usage
if __name__ == "__main__":
    extractor = SpotifyExtractor()
    
    # Get recent tracks
    tracks_df = extractor.get_recently_played(limit=50)
    print(f"Extracted {len(tracks_df)} tracks")
    
    # Get audio features
    track_ids = tracks_df['track_id'].tolist()
    features_df = extractor.get_audio_features(track_ids)
    
    # Merge
    final_df = tracks_df.merge(features_df, on='track_id', how='left')
    
    # Save to CSV (temporary)
    final_df.to_csv('data/raw_listening_history.csv', index=False)