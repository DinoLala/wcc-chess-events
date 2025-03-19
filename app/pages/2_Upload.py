import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle 

# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_all_games
# from app.common.functions import get_entry_list,get_pairing,get_standing

import streamlit as st

import requests
import os

st.set_page_config(layout="wide")
def get_uscf_rating(uscf_id):
    url = f"https://www.uschess.org/msa/MbrDtlMain.php?{uscf_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Standard Rating
        rating_table = soup.find_all("table")[2]  # Ratings table is usually the third table
        rows = rating_table.find_all("tr")

        ratings = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                rating_type = cols[0].text.strip()
                rating_value = cols[1].text.strip()
                
                ratings[rating_type] = rating_value

        # Extract useful ratings
        rating_categories = ["Regular Rating", "Quick Rating", "Blitz Rating"]
        result = {key: ratings[key] for key in rating_categories if key in ratings}
        current_rating=ratings["Regular Rating"][:4].split('\\')[0]
        # print(current_rating)

        return current_rating if result else "No rating found"
    
    else:
        return "Invalid USCF ID or connection issue"

def get_update_rating(df):
    col1, col2 = st.columns([3,3])
    
    with col1:
        st.write('## :orange[file uploaded]')
        
        st.dataframe(df)  # Interactive table
    if st.button("Update rating"):
        with col2:
            df['rating']=df['uscf_id'].apply(lambda x: get_uscf_rating(x))
            st.write('## :blue[Current month rating]')
            # df_updated=df[['tournament', 'section','player','updated_rating']]
            st.dataframe(df)


def get_upload_entry_list(df):
    st.write('## :orange[file uploaded]')
        
    st.dataframe(df)  # Interactive table
    if st.button("Confirmed"):
       df.to_csv('./app/data/tournaments/current_tournament/entry_list.csv')
       st.write('### :orange[Entry list saved]')


col1, col2, col3 = st.columns([2,2,2])
upload_option_list=['Update rating','Entry list','Pairing','Standing','Grandpix']
with col1:
    upload_option = st.selectbox("File to upload:", list(upload_option_list))


# File uploader widget
st.subheader(f"📂 Upload and View a CSV File for: :red[{upload_option}]")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    
    # Read CSV into Pandas DataFrame
    df = pd.read_csv(uploaded_file)
    df.columns=[c.lower() for c in df.columns]

    # Display the DataFrame
    if upload_option =='Update rating':
        get_update_rating(df)
    elif upload_option =='Entry list':
        get_upload_entry_list(df)
        
           

