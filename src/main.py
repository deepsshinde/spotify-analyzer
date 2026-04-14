"""
Main pipeline script to extract, load, and transform Spotify data
Run this daily or whenever you want to update your data
"""

import sys
from extract.spotify_extractor import SpotifyExtractor
from load.db_loader import DBLoader
import pandas as pd
from datetime import datetime

def run_pipeline():
    """Run the complete ETL pipeline"""
    
    print("="*50)
    print("🎵 Starting Spotify Analytics Pipeline")
    print("="*50)
    
    try:
        # STEP 1: Extract data from Spotify
        print("\n[1/3] 📥 Extracting data from Spotify API...")
        extractor = SpotifyExtractor()
        
        # Get recently played tracks
        tracks_df = extractor.get_recently_played(limit=50)
        print(f"   ✅ Extracted {len(tracks_df)} tracks")
        
        # Get audio features
        print("   🎼 Fetching audio features...")
        track_ids = tracks_df['track_id'].tolist()
        features_df = extractor.get_audio_features(track_ids)
        print(f"   ✅ Got features for {len(features_df)} tracks")
        
        # Merge data
        final_df = tracks_df.merge(features_df, on='track_id', how='left')
        
        # STEP 2: Load to database
        print("\n[2/3] 💾 Loading data to PostgreSQL...")
        loader = DBLoader()
        loader.load_data(final_df, 'raw_listening_history')
        print("   ✅ Data loaded successfully")
        
        # STEP 3: Run dbt transformations
        print("\n[3/3] 🔄 Running dbt transformations...")
        import subprocess
        result = subprocess.run(
            ['dbt', 'run', '--project-dir', 'dbt_project'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("   ✅ dbt models executed successfully")
        else:
            print(f"   ❌ dbt failed: {result.stderr}")
            return False
        
        print("\n" + "="*50)
        print("✅ Pipeline completed successfully!")
        print(f"📊 Total records processed: {len(final_df)}")
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)