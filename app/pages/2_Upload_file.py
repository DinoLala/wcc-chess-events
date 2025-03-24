
import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


with open('./app/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# Pre-hashing all plain text passwords once
# st.write(stauth.Hasher.hash_passwords(config['credentials']))

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name']
)
# Creating a login widget
authentication_status = authenticator.login()


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

def get_upload_pairing(df):
    st.write('## :orange[ Pairing file uploaded]')
    col_keep=['tournament','section','round','bd','res','white','res.1','black']
    
    st.dataframe(df)  # Interactive table
    is_subset = set(col_keep).issubset(set(df.columns))
    
    if is_subset:
        round_value=df['round'].value_counts().reset_index()
        tourname_name=df['tournament'].max()
        if len(round_value)>1:
            st.write('### :red[more than 1 round paired]')
        else :
            st.write('## :green[Review and confirm]')
            round_num=round_value['round'].to_list()[0]
            st.write(round_num,tourname_name)
            if st.button(f"Confirmed {round_num} pairing"):
                df[col_keep].to_csv(f'./app/data/tournaments/current_tournament/{round_num}_pairing.csv')
                st.write(f'### :green[Pairing for {round_num} saved]')
                # union with all_pairing file
                uploaded_file ="./app/data/tournaments/current_tournament/pairing_all.csv"
                if round_num==1:
                    df[col_keep].to_csv(f'./app/data/tournaments/current_tournament/pairing_all.csv')
                else:
                    try:
                        df_all = pd.read_csv(uploaded_file)
                        df_all.columns=[c.lower() for c in df_all.columns]
                        # st.write(df_all[col_keep])
                        df_all=df_all.loc[(df_all['tournament']==tourname_name )& (df_all['round'] != round_num)]
                        df_to_save=pd.concat([df_all[col_keep], df[col_keep]], axis=0)
                        df_to_save[col_keep].to_csv(f'./app/data/tournaments/current_tournament/pairing_all.csv')
                    
                        # st.write('### :orange[Entry list saved]')
                    except:
                        st.write('### :orange[Conflict information in pairing file, restart by uploading from round1]')


    else:
        st.write('## :red[file is not in correct format]')
        




def get_upload_standing(df):
    st.write('## :orange[standing file uploaded]')
        
    st.dataframe(df)  # Interactive table
    if st.button("Confirmed"):
       df.to_csv("./app/data/tournaments/current_tournament/standing_all.csv")
       st.write('### :orange[Standing saved]')

def get_upload_grandprix(df):
    st.write('## :orange[Grand Prix standing file uploaded]')
        
    st.dataframe(df)  # Interactive table
    if st.button("Confirmed"):
       df.to_csv("./app/data/tournaments/current_tournament/grandprix_standing_all.csv")
       st.write('### :orange[Grand Prix standing saved]')
def get_upload_tour_info():
    st.write('### :red[Upload Tournament information]')
    user_text = st.text_area("Enter your text here:", height=200)

    st.write("Information:")
    st.write(user_text)
        

    if st.button("Confirmed"):
        with open("./app/data/tournaments/current_tournament/Tournament_info.txt", "w") as file:
            file.write(user_text)
            st.write('### :orange[Tournament information saved]')

def main():
    col1, col2, col3 = st.columns([2,2,2])
    upload_option_list=['Tournament Information','Update rating','Entry list','Pairing','Standing','Grand Prix']
    with col1:
        upload_option = st.selectbox("Upload option:", list(upload_option_list))

    if upload_option =='Tournament Information':
            get_upload_tour_info()
    else:
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
            elif upload_option =='Pairing':
                get_upload_pairing(df)
                # st.write(df.columns)
            elif upload_option =='Standing':
                get_upload_standing(df)
                # st.write(df.columns)
            elif upload_option =='Grand Prix':
                get_upload_grandprix(df)
                # st.write(df.columns)
            
            
            
            
if __name__ == "__main__":
    


    if st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")

    elif st.session_state["authentication_status"] == True:

        st.title('Upload file...')
        main()


