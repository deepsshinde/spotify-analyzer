SELECT
    played_date,
    COUNT(*) as total_tracks_played,
    COUNT(DISTINCT artist_name) as unique_artists,
    ROUND(AVG(energy), 2) as avg_energy,
    ROUND(AVG(danceability), 2) as avg_danceability,
    ROUND(SUM(duration_ms) / 60000.0, 2) as total_minutes_listened
FROM {{ ref('stg_listening_history') }}
GROUP BY played_date
ORDER BY played_date DESC