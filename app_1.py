import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt
import json

# Page title
st.title(' 🏋🏻🏃🏻‍♀️ Visualizations of French Athletes Data')

# Subtitle with expandable content for dataset overview
with st.expander("Dataset Overview"):
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
    df = pd.merge(df1, df_excel, on=['slug', 'firstname', 'lastname'], how='outer')   

    # Fill missing medal values for Antoine Brizard
    df.at[737, 'or2024'] = 1
    df.at[737, 'argent2024'] = 0
    df.at[737, 'bronze 2024'] = 0
    df.at[737, 'total2024'] = 1

    # Fill missing values with 0
    df.fillna(0, inplace=True)

    st.write(df)

st.subheader('1️⃣ Metrics of French Athletes in this Dataset')
tab1, tab2, tab3, tab4 = st.columns(4)

# Total number of athletes
total_athletes = len(df)
tab1.metric("Total Athletes", total_athletes)

# Total number of Paralympic athletes
athletespara = df['type'] == 'paralympic'
tab2.metric("Total Paralympic Athletes", athletespara.sum())

# Total number of Olympic athletes
athletesolympic = df['type'] == 'olympic'
tab3.metric("Total Olympic Athletes", athletesolympic.sum())

# Total number of medalists
medalist = df['total2024'].sum()
tab4.metric("Total Medalists in 2024", medalist)


# Age Distribution and Youngest/Oldest Athletes
df['age'] = pd.to_datetime(df['birthdate']).apply(lambda x: 2024 - x.year)

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
youngest_athletes = df.nsmallest(3, 'age')
for i, col in enumerate([col1, col2, col3]):
    row = youngest_athletes.iloc[i]
    col.markdown(generate_athlete_card(row), unsafe_allow_html=True)

# Display the 3 Oldest Athletes
tab2.subheader('The 3 Oldest Athletes')
col4, col5, col6 = tab2.columns(3)
oldest_athletes = df.nlargest(3, 'age')
for i, col in enumerate([col4, col5, col6]):
    row = oldest_athletes.iloc[i]
    col.markdown(generate_athlete_card(row), unsafe_allow_html=True)

# Number of Athletes in each Discipline
st.subheader('3️⃣ Number of athletes in each Discipline')
tab1, tab2 = st.tabs(["🏋🏻‍♀️ Paralympic Athletes", "🏃🏻‍♀️ Olympic Athletes"])

with tab1:
    st.subheader('Paralympic Athletes')
    para_disciplines = df[df['type'] == 'paralympic']['disciplines'].explode().value_counts()
    st.bar_chart(para_disciplines)

with tab2:
    st.subheader('Olympic Athletes')
    olympic_disciplines = df[df['type'] == 'olympic']['disciplines'].explode().value_counts()
    st.bar_chart(olympic_disciplines)


# Age Distribution of Athletes
st.subheader('4️⃣ Age Distribution of Athletes')
age_distribution = df['age'].value_counts().sort_index()
age_distribution_df = pd.DataFrame({
    'Age': age_distribution.index,
    'Distribution': age_distribution.values
})
age_distribution_df.set_index('Age', inplace=True)
st.line_chart(age_distribution_df)


# Average Age per Discipline
st.subheader('5️⃣ Average Age of Athletes by Discipline')
tab3, tab4 = st.tabs(["🏋🏻‍♀️ Paralympic Athletes", "🏃🏻‍♀️ Olympic Athletes"])

with tab4:
    st.subheader('Paralympic Athletes')
    para_athletes = df[df['type'] == 'paralympic']
    para_athletes_exploded = para_athletes.explode('disciplines')
    para_avg_age = para_athletes_exploded.groupby('disciplines')['age'].mean()
    st.bar_chart(para_avg_age)

with tab3:
    st.subheader('Olympic Athletes')
    olympic_athletes = df[df['type'] == 'olympic']
    olympic_athletes_exploded = olympic_athletes.explode('disciplines')
    olympic_avg_age = olympic_athletes_exploded.groupby('disciplines')['age'].mean()
    st.bar_chart(olympic_avg_age)


# Top 3 Athletes with the Most Gold Medals in 2024
st.subheader('6️⃣ Top 3 Athletes with the Most Gold Medals in 2024')

# Extract the top 3 athletes with the most gold medals
top_medalists = df.nlargest(3, 'or2024')
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
df['disciplines_str'] = df['disciplines'].apply(lambda x: ', '.join(x) if isinstance(x, list) else 'N/A')
st.subheader('7️⃣ Discipline with the Most Medals in 2024')
discipline_medals = df.groupby('disciplines_str')['total2024'].sum().sort_values(ascending=False)
st.bar_chart(discipline_medals.head(10))


