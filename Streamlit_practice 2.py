import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualizations Uber data", 
                   page_icon="🚗", 
                   layout="wide")

# Using object notation
with st.sidebar:
    st.image("IMG_7046.png", width=150)
    st.title("👩🏼‍🎓 Albane COIFFE")
    st.header("Data Science student, master 1 at EFREI")
    st.markdown("Promo: 2026")

    st.write("This is a Streamlit dashboard to explore Uber data from January 2015.")
    st.markdown('📧: albanecoiffe@gmail.com')
    st.markdown('🌐: [LinkedIn]( www.linkedin.com/in/albane-coiffe)')
    st.markdown('🌐: [GitHub](https://github.com/albanecoiffe)')
    #pdfFileObj = open('./file/CV_Maelwenn_Labidurie.pdf', 'rb')

st.title('🚗 Visualizations Uber data')

st.header("Uber data from January 2015")

# Load the data
path = 'nyc_trips.csv'
data = pd.read_csv(path, delimiter = ',')

# Afficher les données
st.write(data)

st.header('Data visualization')

# number of passager, courses and trips per hour
st.subheader('1️⃣ Number of passengers, courses and trips per hour')
tab1, tab3 , tab2 = st.tabs(["📈 Line Chart", "📈 Bar Chart", "🗃 Data"])

tab1.write('Line chart of number of passengers, courses, tips and total distance per hour')

passenger_by_hour = data.groupby('hour')['passenger_count'].sum()
nb_course = data.groupby('hour').size()
tips = data.groupby('hour')['tip_amount'].sum()
Dist = data.groupby('hour')['trip_distance'].sum()

chart_data = pd.DataFrame({
    'hour': passenger_by_hour.index,
    'Number of passengers': passenger_by_hour.values,
    'Number of courses': nb_course.values,
    'Tips' : tips.values,
    'Distance': Dist.values
})

tab1.line_chart(chart_data.set_index('hour'))

tab3.write("Bar chart of number of passengers, courses, tips, total distance per hour")

chart_data = pd.DataFrame({
    'hour': passenger_by_hour.index,
    'Number of passengers': passenger_by_hour.values,
    'Number of courses': nb_course.values,
    'Tips': tips.values,
    'Distance': Dist.values
})
tab3.bar_chart(chart_data, x='hour', y=['Number of passengers', 'Number of courses', 'Tips', 'Distance'])

tab2.write('Data of number of passengers, courses, tips and distance total per hour')
tab2.write(chart_data)

# Metrics at 10 pm
st.subheader('2️⃣ Metrics at 10 pm')
dist22 = data[data['hour'] == 22]['trip_distance'].sum()
tips22 = data[data['hour'] == 22]['tip_amount'].sum()
nb_course22 = data[data['hour'] == 22].shape[0]
passenger22 = data[data['hour'] == 22]['passenger_count'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='Total distance', value=dist22)
col2.metric(label='Total tips', value=tips22)
col3.metric(label='Total number of courses', value=nb_course22)
col4.metric(label='Total number of passengers', value=passenger22)

# Metrics at 4 am
st.subheader('3️⃣ Metrics at 4 am')
dist4 = data[data['hour'] == 4]['trip_distance'].sum()
tips4 = data[data['hour'] == 4]['tip_amount'].sum()
nb_course4 = data[data['hour'] == 4].shape[0]
passenger4 = data[data['hour'] == 4]['passenger_count'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='Total distance', value=dist4)
col2.metric(label='Total tips', value=tips4)
col3.metric(label='Total number of courses', value=nb_course4)
col4.metric(label='Total number of passengers', value=passenger4)

# Fare amount distribution by trip distance:
st.subheader('4️⃣ Fare amount distribution by trip distance')
tab1, tab2 = st.tabs(["📈 Line Chart", "📈 Bar Chart"
                      ])

tab1.write('Line chart of fare amount distribution by trip distance')
chart_data = data.groupby('trip_distance')['fare_amount'].mean().reset_index()
#utilisation de altair pour nommer les axes
chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X('trip_distance', title='trip distance'),
    y=alt.Y('fare_amount', title='mean fare amount')
)
tab1.altair_chart(chart, use_container_width=True)

tab2.write('Bar chart of fare amount distribution by trip distance')
tab2.bar_chart(chart_data, x='trip_distance', y='fare_amount')

# Means of fare amount, tip amount and total amount by hour
st.subheader('5️⃣ Means of fare amount, tip amount and total amount by hour')

tab1, tab2 = st.tabs(["📈 Line Chart", "📈 Bar Chart"
                      ])

tab1.write('Line chart of means of fare amount, tip amount and total amount by hour')
chart_data = data.groupby('hour')[['fare_amount', 'tip_amount', 'total_amount']].mean().reset_index()
chart_data = pd.melt(chart_data, id_vars='hour', value_vars=['fare_amount', 'tip_amount', 'total_amount'], var_name='amount', value_name='mean amount')

chart_data = pd.DataFrame({
    'fare_amount': data.groupby('hour')['fare_amount'].mean(),
    'tip_amount': data.groupby('hour')['tip_amount'].mean(),
    'total_amount': data.groupby('hour')['total_amount'].mean(),
    'hour': data['hour'].unique()
})

tab1.line_chart(chart_data.set_index('hour'))

tab2.write('Bar chart of means of fare amount, tip amount and total amount by hour')
tab2.bar_chart(chart_data, x='hour', y=['fare_amount', 'tip_amount', 'total_amount'])

# Average speed of trips by hour
st.subheader('6️⃣ Average speed (miles per minute) of trips by hour')
data['trip_duration'] = (pd.to_datetime(data['tpep_dropoff_datetime']) - pd.to_datetime(data['tpep_pickup_datetime'])).dt.total_seconds() / 60 #miles per minute
data = data[data['trip_duration'] > 0]
data['average_speed'] = data['trip_distance'] / data['trip_duration']
speed_by_hour = data.groupby('hour')['average_speed'].mean().reset_index()

tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "📈 Bar Chart", "🗃 Data"])

tab1.write('Line chart of average speed of trips by hour')
tab1.line_chart(speed_by_hour.set_index('hour'))

tab2.write('Bar chart of average speed of trips by hour')
tab2.bar_chart(speed_by_hour, x='hour', y='average_speed')

tab3.write('Data of average speed of trips by hour')
tab3.write(speed_by_hour)



# map of the trips pickup and dropoff
st.header('Map of the trips (pickup and dropoff)')
tab4, tab5 = st.tabs(["📈 map 1", "📈 map 2"])


# Combiner les coordonnées de départ et d'arrivée dans un seul DataFrame
pickup_points = data[['pickup_latitude', 'pickup_longitude']].rename(columns={
    'pickup_latitude': 'latitude',
    'pickup_longitude': 'longitude'
})
dropoff_points = data[['dropoff_latitude', 'dropoff_longitude']].rename(columns={
    'dropoff_latitude': 'latitude',
    'dropoff_longitude': 'longitude'
})

# Combiner les deux DataFrames
all_points = pd.concat([pickup_points, dropoff_points])

# Afficher la carte avec tous les points
tab4.write('Map 1 of the trips')
tab4.map(all_points)


chart_data = data[['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude']]
tab5.write('Map 2 of the trips with pydeck')
tab5.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=40.73061,
        longitude=-73.935242,
        zoom=10,
        pitch=50,
    ),

    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[pickup_longitude, pickup_latitude]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[dropoff_longitude, dropoff_latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],

))