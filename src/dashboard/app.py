import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="🎵 My Spotify Analytics", layout="wide")

# Database connection
@st.cache_resource
def get_db_connection():
    db_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    return create_engine(db_string)

engine = get_db_connection()

# Load data
@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM stg_listening_history ORDER BY played_at DESC"
    return pd.read_sql(query, engine)

# Main app
st.title("🎵 My Spotify Listening Analytics")
st.markdown("---")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['played_date'].min(), df['played_date'].max())
)

# Filter data
filtered_df = df[
    (df['played_date'] >= pd.to_datetime(date_range[0])) &
    (df['played_date'] <= pd.to_datetime(date_range[1]))
]

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tracks", len(filtered_df))

with col2:
    st.metric("Unique Artists", filtered_df['artist_name'].nunique())

with col3:
    hours = filtered_df['duration_ms'].sum() / (1000 * 60 * 60)
    st.metric("Hours Listened", f"{hours:.1f}")

with col4:
    avg_energy = filtered_df['energy'].mean()
    st.metric("Avg Energy", f"{avg_energy:.2f}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Listening Over Time")
    daily_plays = filtered_df.groupby('played_date').size().reset_index(name='plays')
    fig = px.line(daily_plays, x='played_date', y='plays', 
                  title="Daily Plays")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎤 Top 10 Artists")
    top_artists = filtered_df['artist_name'].value_counts().head(10)
    fig = px.bar(top_artists, orientation='h', 
                 title="Most Played Artists")
    st.plotly_chart(fig, use_container_width=True)

# Audio features analysis
st.markdown("---")
st.subheader("🎼 Audio Features Analysis")

col1, col2 = st.columns(2)

with col1:
    # Energy vs Danceability scatter
    fig = px.scatter(filtered_df, x='energy', y='danceability',
                     hover_data=['track_name', 'artist_name'],
                     title="Energy vs Danceability",
                     color='valence',
                     color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Listening by hour
    hourly = filtered_df.groupby('played_hour').size().reset_index(name='plays')
    fig = px.bar(hourly, x='played_hour', y='plays',
                 title="Listening by Hour of Day")
    st.plotly_chart(fig, use_container_width=True)

# Recent tracks table
st.markdown("---")
st.subheader("🎵 Recent Tracks")
st.dataframe(
    filtered_df[['played_at', 'track_name', 'artist_name', 'energy', 'danceability']]
    .head(20),
    use_container_width=True
)