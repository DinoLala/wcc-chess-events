import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st


import requests

st.set_page_config(layout="wide")

st.header(':orange[Have fun solving puzzles with us !]')

st.header('')
            
import os

col1,col2 = st.columns(2)

if 'counter' not in st.session_state: 
    st.session_state.counter = 0

def showPhoto(photo):
    # col2.image(photo,caption=photo)
    col2.image(photo)
    # col1.write(f"Index as a session_state attribute: {st.session_state.counter}")
    if 'ww' in photo:
        col1.subheader(f"White to move and win")
    elif "wd" in photo:
        col1.subheader(f"White to move and draw")

    
    ## Increments the counter to get next photo
    st.session_state.counter += 1
    if st.session_state.counter >= len(pathsImages):
        st.session_state.counter = 0

# Get list of images in folder
# folderWithImages = r"images"
folderWithImages = r"app/data/puzzles"

pathsImages = [os.path.join(folderWithImages,f) for f in os.listdir(folderWithImages)]

# col1.subheader("List of images in folder")

# col1.write(pathsImages)

# Select photo a send it to button
photo = pathsImages[st.session_state.counter]
show_btn = col1.button("Show next puzzle ⏭️",on_click=showPhoto,args=([photo]))