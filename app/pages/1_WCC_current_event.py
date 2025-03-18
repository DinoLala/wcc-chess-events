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


st.set_page_config(layout="wide")


def get_entry_list():
    
    uploaded_file = "./app/data/tournaments/current_tournament/entry_list.csv"

    
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        tourname_name=df['tournament'][1]
        st.subheader(f"Entry list for {tourname_name}:")


        df['player'] = df[['player','uscf_id']].apply(lambda x: f'<a href="https://www.uschess.org/msa/MbrDtlMain.php?{int(x[1])}" target="_blank">{x[0]}</a>', axis=1)

        # Display the DataFrame with hyperlinks
        table_style = """
        <style>
        .dataframe {
            width: 500px;  /* Adjust width of the table */
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
        # st.markdown(table_style, unsafe_allow_html=True)
        styled_table = df[['player','rating','section']].to_html(escape=False)
        # Custom CSS for header color (orange)
        styled_table = styled_table.replace(
            '<thead>',
            '<thead style="background-color: green; color: orange;">'
        )

        st.markdown(styled_table, unsafe_allow_html=True)

def get_pairing(df,df_all,uploaded_file, section):
    TABLE_STYLE = """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    text-align: center;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
                button {
                    padding: 5px 10px;
                    font-size: 14px;
                }
            </style>
        """

    st.markdown(TABLE_STYLE, unsafe_allow_html=True)

    # Store table in session state to persist updates
    if 'open' in section:
        pairing_table="pairing_table_open"
        if pairing_table not in st.session_state:
            
            st.session_state[pairing_table] = df.copy()
    else:
        pairing_table="pairing_table_u1600"
        if "pairing_table_u1600" not in st.session_state:
            
            st.session_state[pairing_table] = df.copy()
            # st.session_state.pairing_table_u1600 = df.copy()

    if "selected_row" not in st.session_state:
        st.session_state.selected_row = None  # To track which row's button was clicked

    # Display the pairing table
    st.subheader("Pairing Table")
    table_html = """<table><tr><th>Bd</th>
                    <th>Res</th>
                    <th>White</th>
                    <th>Res.1</th>
                    <th>Black</th>
                    <th>Enter Result</th>
                    </tr>"""

    # Table layout
    col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1,2,1])

    with col1:
        st.write("**Bd**")
    with col2:
        st.write("**res**")
    with col3:
        st.write("**Player1**")
    with col4:
        st.write("**res.1**")
    with col5:
        st.write("**player2**")
    with col6:
        st.write("**Enter Result**")
    

    # Iterate through the rows and add input fields & buttons
    for index, row in st.session_state[pairing_table].iterrows():
        # st.write(index,row)
        
        col1, col2, col3, col4,col5,col6= st.columns([1, 1, 2, 1,2, 1])
        
        with col1:
            st.write(row["Bd"])
        with col2:
            st.write(row["Res"])
        with col3:
            st.write(row["White"])
        with col4:
            st.write(row["Res.1"])
        with col5:
            st.write(row["Black"])
        with col6:
            if st.button(f"Enter Result", key=section+f"btn_{index}"):
                st.session_state.selected_row = index  # Store selected row index

    # Open modal when a row is selected
    if st.session_state.selected_row is not None:
        index_1=st.session_state.selected_row
        # with st.expander(f"Enter Result for {st.session_state[pairing_table].at[st.session_state.selected_row, 'White']} vs {st.session_state[pairing_table].at[st.session_state.selected_row, 'Black']}"):
        with st.popover(f"Enter Result for {st.session_state[pairing_table].at[st.session_state.selected_row, 'White']} vs {st.session_state[pairing_table].at[st.session_state.selected_row, 'Black']}"):
        # with st.popover(f"Enter Result"):
            new_result = st.text_input("Enter Match Result:", key=section+"result_input")
            if st.button(section+"Save Result"):
                # Update the result in session state
                if new_result!=.5:
                    st.session_state[pairing_table].at[st.session_state.selected_row, "Res"] = str(new_result)
                    st.session_state[pairing_table].at[st.session_state.selected_row, "Res.1"] = str(1-float(new_result))
                else:
                    st.session_state[pairing_table].at[st.session_state.selected_row, "Res"] = '.5'
                    st.session_state[pairing_table].at[st.session_state.selected_row, "Res.1"] = ".5"

                if st.session_state[pairing_table].at[st.session_state.selected_row, "Black"]=='BYE':
                    st.session_state[pairing_table].at[st.session_state.selected_row, "Res.1"] = ''

                
                tb=st.session_state[pairing_table].at[st.session_state.selected_row, "Bd"] 
                
                df_all.at[ index_1, 'Res'] = str(new_result)
                df_all.at[ index_1, 'Res.1'] = str(1-float(new_result))
                df_all.loc[df_all['Black'] == 'BYE', 'Res.1'] = '9999999'
                df_all=df_all.replace('9999999','').replace(9999999,'')
                # st.write(df.loc[df['Bd'] == tb])
                df_all.to_csv(uploaded_file)
                st.session_state.selected_row = None  # Close modal
                # st.experimental_rerun()
                st.rerun()  # Rerun app to update table
               

            

def get_standing(tournament, section,uploaded_file):
    

    df = pd.read_csv(uploaded_file)

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        df = df.fillna('')
        # Display the DataFrame with hyperlinks
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
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

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
