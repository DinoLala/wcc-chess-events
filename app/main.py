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
Duy_chess_note='https://docs.google.com/spreadsheets/d/10Lfybi_B-zMD2yyJdxc6Kos1qRIaEHC5dDKvz3OZJwU/edit?gid=0#gid=0'

capital_area_chess="https://www.capitalareachess.com/"
uscf_top100="https://www.uschess.org/component/option,com_top_players/Itemid,371/"
fide_profile='https://ratings.fide.com/profile/39956741'
boyston_beta="https://beta.boylstonchess.org/events"
st.write(":orange[For plan ahead USCF [Tournaments ](%s)]" % plan_ahead)

st.write(":orange[For MACA [Tournaments ](%s)]" % maca_tournament)
st.write(":green[For MACA [Tournaments result links ](%s)]" % maca_oldtour_result)

st.write(":orange[For Boylston [Tournaments beta links ](%s)]" % boyston_beta)

st.write(":green[For Continental Chess Association [Tournaments ](%s)]" % continental_tour)

st.write(":orange[For Capital Area Ches [Tournaments ](%s)]" % capital_area_chess) 

st.write(":green[USCF top 100 [uscf top 100 ](%s)]" % uscf_top100) 
st.write(":orange[Fide Profile [Fide Profile ](%s)]" % fide_profile) 

st.write(":green[Duy Chess note [note ](%s)]" % Duy_chess_note)