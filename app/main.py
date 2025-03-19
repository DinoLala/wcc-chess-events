import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd


import streamlit as st


# st.subheader('For more information, please visit US Chess official website')
col1, col2=st.columns(2)
with col1:
    st.header(':orange[Play, Learn & Enjoy!]')
   
with col2:
    st.image('./app/data/chess2.png')

url = "https://new.uschess.org/"
plan_ahead="https://new.uschess.org/plan-ahead-calendar"
# st.write("check out this [link](%s)" % url)
st.write(":blue[For more information, please visit US Chess official [website ](%s)]" % url)

maca_tournament = "http://www.masschess.org/Events/chess-event-calendar.aspx"
st.write(":blue[Massachusetts Chess Association [website ](%s)]" % maca_tournament)

wcc_tournament = "http://www.wachusettchess.org/index.php"
st.write(":blue[Wachusett Chess Club [website ](%s)]" % wcc_tournament)

maca_oldtour_result="https://www.uschess.org/msa/AffDtlTnmtHst.php?T5000181"

continental_tour="http://www.chesstour.com/refs.html"
