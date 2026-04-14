-- Raw listening history
CREATE TABLE raw_listening_history (
    id SERIAL PRIMARY KEY,
    played_at TIMESTAMP,
    track_id VARCHAR(255),
    track_name VARCHAR(500),
    artist_name VARCHAR(500),
    album_name VARCHAR(500),
    duration_ms INTEGER,
    danceability FLOAT,
    energy FLOAT,
    tempo FLOAT,
    valence FLOAT,
    acousticness FLOAT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX idx_played_at ON raw_listening_history(played_at);
CREATE INDEX idx_track_id ON raw_listening_history(track_id);