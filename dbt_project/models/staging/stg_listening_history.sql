WITH source AS (
    SELECT * FROM {{ source('spotify', 'raw_listening_history') }}
),

cleaned AS (
    SELECT
        id,
        played_at,
        track_id,
        track_name,
        artist_name,
        album_name,
        duration_ms,
        ROUND(danceability::numeric, 2) as danceability,
        ROUND(energy::numeric, 2) as energy,
        ROUND(tempo::numeric, 2) as tempo,
        ROUND(valence::numeric, 2) as valence,
        DATE(played_at) as played_date,
        EXTRACT(HOUR FROM played_at) as played_hour,
        loaded_at
    FROM source
    WHERE track_id IS NOT NULL
)

SELECT * FROM cleaned