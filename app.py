import streamlit as st
import pandas as pd
import json

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
    - 🏅 **French Olympic and Paralympic athletes**: Explore athlete profiles, their disciplines, and their medal tallies.
    - 🗺️ **Map of French athletes**: Visualize the geographical spread of athletes across different disciplines.
    - 🔥 **Torch position**: Track the current location of the Olympic torch across France.
    """)
    
    # French Athletes Data
    st.subheader("📊 French Olympic and Paralympic Athletes Data")
    
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
    
    # Clean-up and display the athlete data
    df1 = df1.drop(columns=['_geoloc', 'isMedalist'])
    
    # Load medal data
    df_excel = pd.read_excel("medailles2024.xlsx")
    df = pd.merge(df1, df_excel, on=['slug', 'firstname', 'lastname'], how='outer')   
    df.fillna(0, inplace=True)
    
    # Display updated athlete data with medals
    st.write(df)

    # Torch Relay Data
    st.subheader("🔥 Torch Relay Position")
    df_torch = pd.read_excel("games_map_torch_position.xlsx", dtype={'lat': float, 'lon': float})
    st.dataframe(df_torch.head())  # Display first 5 rows of torch relay data
