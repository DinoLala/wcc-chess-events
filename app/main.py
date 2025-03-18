import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd


import streamlit as st


# st.subheader('For more information, please visit US Chess official website')
col1, col2=st.columns(2)
with col1:
    st.header(':orange[Having Fun with Chess!!]')
   
with col2:
    st.image('./app/data/nhan.jpeg')

url = "https://new.uschess.org/"
plan_ahead="https://new.uschess.org/plan-ahead-calendar"
# st.write("check out this [link](%s)" % url)
st.write(":orange[For more information, please visit US Chess official [website ](%s)]" % url)

maca_tournament = "http://www.masschess.org/Events/chess-event-calendar.aspx"

maca_oldtour_result="https://www.uschess.org/msa/AffDtlTnmtHst.php?T5000181"

continental_tour="http://www.chesstour.com/refs.html"
