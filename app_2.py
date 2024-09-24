import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Page title
st.title('🗺️ Map Representing French Athletes')

# Load and display athlete data
file_path = "athlete_fr_2024.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Normalize the 'hits' section (athlete data) into a DataFrame
athletes_data = data['athletes']['hits']
df1 = pd.json_normalize(athletes_data)

# Extract the year of the Olympic Games and slug of the disciplines
df1['olympicGames'] = df1['olympicGames'].apply(lambda x: [game['year'] for game in x] if isinstance(x, list) else None)
df1['disciplines'] = df1['disciplines'].apply(lambda x: [discipline['slug'] for discipline in x] if isinstance(x, list) else None)

# Ensure latitude and longitude columns exist
if '_geoloc.lat' in df1.columns and '_geoloc.lng' in df1.columns:
    df1 = df1.rename(columns={'_geoloc.lat': 'lat', '_geoloc.lng': 'lon'})
else:
    st.error("Latitude and longitude columns are missing.")
    st.write("Available columns:", df1.columns)

# Filter rows that have latitude and longitude values
map_data = df1.dropna(subset=['lat', 'lon'])

# Define the pydeck Layer for geographical visualization
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    pickable=True,  # Enable click events
    get_position='[lon, lat]',  # Specify the positions as [longitude, latitude]
    get_radius=1000,  # Set the base radius to a smaller value for zoom levels
    get_radius_scale=2,  # Scale factor for zooming in and out (optional)
    get_fill_color=[255, 0, 0, 160],  # Use a bright red color
    radius_min_pixels=5,  # Minimum radius when zoomed in
    radius_max_pixels=50,  # Maximum radius when zoomed out
)

# Set the initial view of the map with zoom control
view_state = pdk.ViewState(
    latitude=48.8566,  # Center the map near France
    longitude=2.3522,
    zoom=5,  # Initial zoom level
    pitch=0,
)

# Create the pydeck deck with dynamic point scaling
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{firstname} {lastname}\n{disciplines}"},
)

# Display the map
st.pydeck_chart(r)
st.markdown('Map showing the geographical distribution of athletes based on their latitude and longitude coordinates.')
