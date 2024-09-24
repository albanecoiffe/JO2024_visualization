import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt
import json
import pydeck as pdk


# Page title
st.title('🔥 Map torch position')

# Subtitle with expandable content for dataset overview
with st.expander("Dataset Overview"):
    st.write("""
    This dataset contains information about the position of the torch during the Paris 2024 Olympic and Paralympic Games.
    The columns include details such as latitude and longitude.
    """)
    file_path = "games_map_torch_position.xlsx"
    with open(file_path, 'r') as file:
        df = pd.read_excel(file_path, dtype={'latitude': float, 'longitude': float})
    st.write(df)

# map of the torch position
st.subheader('1️⃣ Map of the torch position')
df = df.dropna(subset=['latitude', 'longitude'])

# with .map
st.map(df)


