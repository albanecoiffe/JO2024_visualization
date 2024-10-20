import streamlit as st
import pandas as pd
import numpy as np
import json
import altair as alt
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt
import pydeck as pdk


# Page configuration (called only once, at the top)
st.set_page_config(page_title="Paris JO 2024 Dashboard", 
                   page_icon="🏆", 
                   layout="wide")

# Sidebar with personal info and filtering options
with st.sidebar:
    st.image("IMG_7046.png", width=150)
    st.title("👩🏼‍🎓 Albane COIFFE")
    st.header("Data Science student, master 1 at EFREI")
    st.markdown("Promo: 2026")
    st.write("This is a Streamlit dashboard to explore Paris JO 2024 data.")
    st.markdown('📧: albanecoiffe@gmail.com')
    st.markdown('🌐: [LinkedIn](https://www.linkedin.com/in/albane-coiffe)')
    st.markdown('🌐: [GitHub](https://github.com/albanecoiffe)')

    # Navigation buttons
    st.subheader("Navigation")
    app_1 = st.button("🏅 French athletes")
    app_2 = st.button("🗺️ Map of French athletes")
    app_3 = st.button("🔥 Torch position")
    main = st.button("🏠 Back to the main page")

# Function to execute and display content of a Python file
def execute_python_file(filepath):
    try:
        with open(filepath, 'r') as file:
            file_content = file.read()
            exec(file_content, globals())  # Execute the content of the file
    except Exception as e:
        st.error(f"Error executing the file {filepath}: {e}")

# Navigation logic
if app_1:
    execute_python_file("app_1.py")  # Executes app_1.py
elif app_2:
    execute_python_file("app_2.py")  # Executes app_2.py
elif app_3:
    execute_python_file("app_3.py")  # Executes app_3.py
else:
    # Main homepage
    st.title('🏆 Paris JO 2024 - Data Visualization Project')
    st.markdown("""
    **Welcome to the Paris 2024 Olympic Games data visualization dashboard.** 
    This project is developed as part of a *Data Visualization* course, and it showcases data from the 
    **Paris 2024 Olympic and Paralympic Games**, including information about athletes, medals, and the torch relay.
    """)
    
    # Data overview
    st.header("🚀 What this project covers:")
    
    st.markdown("""
    - **French Olympic and Paralympic athletes**: Explore athlete profiles, their disciplines, and their medal tallies.
    - **Map of French athletes**: Visualize the geographical spread of athletes across different disciplines.
    - **Torch position**: Track the current location of the Olympic torch across France.
    """)

    # French Athletes Data with expander
    with st.expander("📊 French Olympic and Paralympic Athletes data"):
        st.write("""
        This dataset contains information about French athletes participating in the Paris 2024 Olympic and Paralympic Games.
        The columns include details such as name, gender, disciplines, Olympic participation, and a link to each athlete's photo.
        """)
        # Load the data
        file_path = "athlete_fr_2024.json"
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Normalize the 'hits' section (athlete data) into a DataFrame
        athletes_data = data['athletes']['hits']
        df1 = pd.json_normalize(athletes_data)

        # Extract the year of the Olympic Games and slug of the disciplines
        df1['olympicGames'] = df1['olympicGames'].apply(lambda x: [game['year'] for game in x] if isinstance(x, list) else None)
        df1['disciplines'] = df1['disciplines'].apply(lambda x: [discipline['slug'] for discipline in x] if isinstance(x, list) else None)
        df1 = df1.drop(columns=['_geoloc', 'isMedalist'])
        
        # Handling missing birthdates
        df1.at[575, 'birthdate'] = "2005-04-08"
        df1.at[129, 'birthdate'] = "2000-01-13"
        df1.at[805, 'birthdate'] = "2003-09-09"
        df1.at[671, 'birthdate'] = "2002-11-20"

        df_excel = pd.read_excel("medailles2024.xlsx")
        # Merge the dataframes on 'slug', 'firstname', and 'lastname'
        df1 = pd.merge(df1, df_excel, on=['slug', 'firstname', 'lastname'], how='outer')   

        # Fill missing medal values for Antoine Brizard
        df1.at[737, 'or2024'] = 1
        df1.at[737, 'argent2024'] = 0
        df1.at[737, 'bronze 2024'] = 0
        df1.at[737, 'total2024'] = 1

        # Fill missing values with 0
        df1.fillna(0, inplace=True)

        st.write(df1)


    # Torch Relay Data with expander
    with st.expander("🔥 Torch Relay Position data"):
        st.write("""
        This dataset contains information about the position of the torch during the Paris 2024 Olympic and Paralympic Games.
        The columns include details such as latitude and longitude.
        """)
        file_path = "games_map_torch_position.xlsx"
        with open(file_path, 'r') as file:
            df2 = pd.read_excel(file_path, dtype={'latitude': float, 'longitude': float})
        st.write(df2)



## Part 2 : Visualizations of French Athletes Data



# Page title
st.title(' 🏋🏻🏃🏻‍♀️ Visualizations of French Athletes Data')

st.subheader('1️⃣ Metrics of French Athletes in this Dataset')
tab1, tab2, tab3, tab4 = st.columns(4)

# Total number of athletes
total_athletes = len(df1)
tab1.metric("Total Athletes", total_athletes)

# Total number of Paralympic athletes
athletespara = df1['type'] == 'paralympic'
tab2.metric("Total Paralympic Athletes", athletespara.sum())

# Total number of Olympic athletes
athletesolympic = df1['type'] == 'olympic'
tab3.metric("Total Olympic Athletes", athletesolympic.sum())

# Total number of medalists
medalist = df1['total2024'].sum()
tab4.metric("Total Medalists in 2024", medalist)


# Age Distribution and Youngest/Oldest Athletes
df1['age'] = pd.to_datetime(df1['birthdate']).apply(lambda x: 2024 - x.year)

st.subheader('2️⃣ The 3 Youngest and Oldest Athletes')
tab1, tab2 = st.tabs(["👶🏻 The 3 Youngest Athletes", "👴🏻 The 3 Oldest Athletes"])

# Helper to generate athlete card
def generate_athlete_card(row):
    disciplines_str = ', '.join(row['disciplines']) if row['disciplines'] else 'N/A'
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; margin-bottom: 30px;">
        <img src="{row['pictureUrl']}" style="width: 150px; height: auto; margin-bottom: 15px;"/>
        <div style="text-align: center; line-height: 1.8; margin-top: 10px;">
            <strong>{row['firstname']} {row['lastname']}</strong><br>
            <span style="margin-top: 5px;">Age: {row['age']}</span><br>
            <span style="margin-top: 5px;">Total Medals JO 2024: {row['total2024']}</span><br>
            <span style="margin-top: 5px;">Discipline JO 2024: {disciplines_str}</span><br>
        </div>
    </div>
    """

# Display the 3 Youngest Athletes
tab1.subheader('The 3 Youngest Athletes')
col1, col2, col3 = tab1.columns(3)
youngest_athletes = df1.nsmallest(3, 'age')
for i, col in enumerate([col1, col2, col3]):
    row = youngest_athletes.iloc[i]
    col.markdown(generate_athlete_card(row), unsafe_allow_html=True)

# Display the 3 Oldest Athletes
tab2.subheader('The 3 Oldest Athletes')
col4, col5, col6 = tab2.columns(3)
oldest_athletes = df1.nlargest(3, 'age')
for i, col in enumerate([col4, col5, col6]):
    row = oldest_athletes.iloc[i]
    col.markdown(generate_athlete_card(row), unsafe_allow_html=True)

# Number of Athletes in each Discipline
st.subheader('3️⃣ Number of athletes in each Discipline')
tab1, tab2 = st.tabs(["🏋🏻‍♀️ Paralympic Athletes", "🏃🏻‍♀️ Olympic Athletes"])

with tab1:
    st.subheader('Paralympic Athletes')
    para_disciplines = df1[df1['type'] == 'paralympic']['disciplines'].explode().value_counts()
    st.bar_chart(para_disciplines)

with tab2:
    st.subheader('Olympic Athletes')
    olympic_disciplines = df1[df1['type'] == 'olympic']['disciplines'].explode().value_counts()
    st.bar_chart(olympic_disciplines)


# Average Age per Discipline
st.subheader('4️⃣ Average Age of Athletes by Discipline')
tab3, tab4 = st.tabs(["🏋🏻‍♀️ Paralympic Athletes", "🏃🏻‍♀️ Olympic Athletes"])

with tab4:
    st.subheader('Paralympic Athletes')
    para_athletes = df1[df1['type'] == 'paralympic']
    para_athletes_exploded = para_athletes.explode('disciplines')
    para_avg_age = para_athletes_exploded.groupby('disciplines')['age'].mean()
    st.bar_chart(para_avg_age)

with tab3:
    st.subheader('Olympic Athletes')
    olympic_athletes = df1[df1['type'] == 'olympic']
    olympic_athletes_exploded = olympic_athletes.explode('disciplines')
    olympic_avg_age = olympic_athletes_exploded.groupby('disciplines')['age'].mean()
    st.bar_chart(olympic_avg_age)


# Top 3 Athletes with the Most Gold Medals in 2024
st.subheader('5️⃣ Top 3 Athletes with the Most Gold Medals in 2024')

# Extract the top 3 athletes with the most gold medals
top_medalists = df1.nlargest(3, 'or2024')
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

# Display top 3 athletes with the most gold medals
for i, col in enumerate([col1, col2, col3]):
    row = top_medalists.iloc[i]
    disciplines_str = ', '.join(row['disciplines']) if row['disciplines'] else 'N/A'
    col.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; margin-bottom: 30px;">
        <img src="{row['pictureUrl']}" style="width: 150px; height: auto; margin-bottom: 15px;"/>
        <div style="text-align: center; line-height: 1.8; margin-top: 10px;">
            <strong>{row['firstname']} {row['lastname']}</strong><br>
            <span style="margin-top: 5px;">Total Medals: {row['total2024']}</span><br>
            <span style="margin-top: 5px;">Gold Medals: {row['or2024']}</span><br>
            <span style="margin-top: 5px;">Silver Medals: {row['argent2024']}</span><br>
            <span style="margin-top: 5px;">Bronze Medals: {row['bronze 2024']}</span><br>
            <span style="margin-top: 5px;">Discipline JO 2024: {disciplines_str}</span><br>
        </div>
    </div>
    """, unsafe_allow_html=True)

# The disipline with the most medals in 2024
df1['disciplines_str'] = df1['disciplines'].apply(lambda x: ', '.join(x) if isinstance(x, list) else 'N/A')
st.subheader('6️⃣ Discipline with the Most Medals in 2024')
discipline_medals = df1.groupby('disciplines_str')['total2024'].sum().sort_values(ascending=False)
st.bar_chart(discipline_medals.head(10))




# Part 3 : Visualizations the geographical distribution of athletes based on their latitude and longitude coordinates


# Page title
st.title('🗺️ Map Representing French Athletes')

# Load athlete data (assuming `data` is already loaded from the previous part)
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

# Add a text input for filtering the athlete by first or last name
search_query = st.text_input("Search for an athlete by first or last name:")

# If a search query is provided, filter the DataFrame
if search_query:
    map_data = map_data[
        (map_data['firstname'].str.contains(search_query, case=False)) | 
        (map_data['lastname'].str.contains(search_query, case=False))
    ]

# Get a list of all available disciplines
all_disciplines = sorted(set([discipline for sublist in df1['disciplines'].dropna() for discipline in sublist]))

# Add a selectbox for selecting a discipline
selected_discipline = st.selectbox("Select a discipline:", ["All disciplines"] + all_disciplines)

# If a discipline is selected, filter the DataFrame
if selected_discipline != "All disciplines":
    map_data = map_data[map_data['disciplines'].apply(lambda x: selected_discipline in x if isinstance(x, list) else False)]

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





# Part 4 : Visualizations of the Torch Position Data





# Page title
st.title('🔥 Dynamic Torch Position Map')

# Convert start_datetime to Pandas datetime format
df2['start_datetime'] = pd.to_datetime(df2['start_datetime'])

# Ensure latitude and longitude columns exist and are of type float
df2 = df2.dropna(subset=['latitude', 'longitude'])
df2['latitude'] = df2['latitude'].astype(float)
df2['longitude'] = df2['longitude'].astype(float)

# Convert the `start_datetime` to a date format for the slider (without time)
df2['date'] = df2['start_datetime'].dt.date

# Create a slider to control the date range (only date without time)
start_date = st.slider(
    "Select the date range", 
    min_value=df2['date'].min(), 
    max_value=df2['date'].max(), 
    value=(df2['date'].min(), df2['date'].max())
)

# Filter the dataframe based on the selected date range
filtered_data = df2[(df2['date'] >= start_date[0]) & (df2['date'] <= start_date[1])]

# Remove any unnecessary or problematic columns
filtered_data = filtered_data[['longitude', 'latitude', 'start_datetime']]  # Keep only necessary columns

# Define the pydeck Layer for the dynamic map
layer = pdk.Layer(
    'ScatterplotLayer',
    data=filtered_data,
    get_position='[longitude, latitude]',
    get_radius=200,  # Set the base radius for the points
    get_color=[255, 0, 0],  # Set the color of the points
    pickable=True,
    radius_min_pixels=5,
    radius_max_pixels=20,
)

# Set the initial view of the map (centered over France)
view_state = pdk.ViewState(
    latitude=48.8566,  # Center over France
    longitude=2.3522,
    zoom=5,
    pitch=0,  # Set pitch to 0 for a straight, 2D map view
)

# Create the pydeck deck
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{start_datetime}"}
)

# Display the map
st.pydeck_chart(r)

st.markdown('This map shows the dynamic path of the Olympic torch over time based on the selected date range.')
