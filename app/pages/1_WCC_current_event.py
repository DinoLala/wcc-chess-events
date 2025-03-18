import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle 

from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_all_games
from app.common.functions import get_entry_list,get_pairing,get_standing

import streamlit as st

import requests


st.set_page_config(layout="wide")



def main():
    st.title(f":blue[Wachusset Chess club tournament]")
    
    # Create tabs

    tab1, tab2, tab3,tab4, tab5 = st.tabs(["Home", "Entry List", 'Pairing','Standing',"Grandpix Table"])
    
    with tab1:
        st.header("Home Page")
    
    with tab2:
        get_entry_list()

    with tab3:
            uploaded_file ="./app/data/tournaments/current_tournament/pairing_all.csv"
            df_all = pd.read_csv(uploaded_file)
            last_round=df_all['round'].max()
            
            st.subheader(f":orange[ Pairing Round {last_round}] ")
            
            tourname_name="2025 George O'Rourke Memorial"
            section_list=set(df_all['section'].to_list())
            section_option = st.selectbox("Choose section:", list(section_list))

            df_all=df_all[['section','round','Bd','Res','White','Res.1','Black']]
            df_all = df_all.fillna('9999999')

            df_all['Bd']=df_all['Bd'].astype('int')
            df_all=df_all.replace('9999999','').replace(9999999,'')

            df=df_all.loc[(df_all['section']==section_option)]
            last_round=df_all['round'].max()
            df=df.loc[df['round']==last_round]
            st.subheader(f"{section_option.upper()} SECTION")
            with st.expander("Click to expand"):
                get_pairing( df,df_all,uploaded_file,section_option)


    with tab4:
        st.title(f"{tourname_name} ")

        standing_uploaded_file = "./app/data/tournaments/current_tournament/standing_all.csv"
        df_standing_all = pd.read_csv(standing_uploaded_file)
        df_standing_all = df_standing_all.fillna('')

        section_list=set(df_standing_all['section'].to_list())

        for section in section_list:
            df_standing_section=df_standing_all.loc[df_standing_all['section']==section]

            with st.expander(f":orange[{section} standing:]"):
                # st.subheader(f":orange[ Standing- Section: {section} Example]")
                table_style = """
                <style>
                .dataframe {
                width: 800px;  /* Adjust width of the table */
                margin-left: auto;
                margin-right: auto;
                }
                th {
                text-align: left;  /* Center the header text */
                }
                td {
                text-align: left;  /* Optional: center-align table data cells */
                }
                </style>
                """
                # Display the styled table with hyperlinks
                st.markdown(table_style, unsafe_allow_html=True)
                st.markdown(df_standing_section.to_html(escape=False), unsafe_allow_html=True)         

    

    with tab5:
        
        st.write('TBD')
        # Sample pairing table data




        
if __name__ == "__main__":
    main()
