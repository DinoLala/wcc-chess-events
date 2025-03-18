import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st


import requests




st.set_page_config(layout="centered")

st.sidebar.header(':orange[USCF Norms sytem:]' )
st.sidebar.write('* Rating 2400: Life Senior Master' )
st.sidebar.write('* Rating 2200: Life Master ' )
st.sidebar.write('* Rating 2000 Candidate Master (C) ' )
st.sidebar.write('* Rating 1800: 1st Category (1)' )
st.sidebar.write('* Rating 1600: 2nd Category (2)' )
st.sidebar.write('* Rating 1400: 3rd Category (3)' )
st.sidebar.write('* Rating 1200: 4th Category (4)' )



st.subheader(':orange[Estimating your post tournament rating:]' )

url = "http://www.glicko.net/ratings/approx.pdf"
# st.write("check out this [link](%s)" % url)
st.write(":orange[Visit [website ](%s) for rating estimation formula]" % url)


# n_win=st.number_input('your pointstest',min_value=0, max_value=3,step=.5)
with st.container():
    # st.write("This is inside the container")
    col1, col2, col3 = st.columns(3)
    with col1:
        current_rating=st.number_input('Your current rating',min_value=.00, max_value=3000.01, )
    with col2:
        n_prior=st.number_input(' #Prior games',min_value=.00, max_value=3000.01,value=50.0,step=1.0 )   
    
    st.divider() 
    st.write(':orange[Tournament result:]' )
    col1, col2, col3 = st.columns(3)
    with col1:
        # current_rating=st.number_input('Your current rating',min_value=.00, max_value=3000.01, )
        tour_rounds=st.number_input('#Tournament games',min_value=.00, max_value=20.01, step=1.0 )
        # tour_rounds=int(tour_rounds)
    with col2:   
        n_win=st.number_input('Your points',min_value=0.0, max_value=tour_rounds,step=.5)
   

    st.write(':orange[Your opponents rating:]' )
    col1, col2, col3 = st.columns(3)
    opponent_list=[]
    with col1:
        #    st.header("A cat")
        
        for r in range(int(tour_rounds/3)+1):
            if r*3+1 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+1),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)


    with col2:
        for r in range(int(tour_rounds/3)+1):
            if r*3+2 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+2),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)
        

    with col3:
        for r in range(int(tour_rounds/3)):
            if r*3+3 <=tour_rounds:
                intput_rating1=st.number_input('Rating '+str(r*3+3),min_value=0, max_value=3000, step=1 )
                opponent_list.append(intput_rating1)
    
    est_submit=st.button('Est Post Rating')
    st.divider() 
    if est_submit:
        
        if current_rating >=2355:
            N_e=n_prior
        elif current_rating >0 and current_rating <2355:
            N_e=min(50/pow(.662+ 0.00000739*pow(2569 - current_rating,2),.5),n_prior)
        else:
            current_rating =0
            N_e=0
        m=tour_rounds
        if (N_e+m) <=0:
            st.write(' invalid inputs')
        else:
            K=800/(N_e+m)
            S=n_win
            E=0
            for p in opponent_list:
                e_p=1/(1+pow(10,-(current_rating-p)/400))
                E=E+e_p
            # get Bonus B
            if tour_rounds <3:
                B=0
            else:
                temp=K*(S-E)
                temp2=14*pow(max(m,4),.5)
                B= max(0, temp-temp2)

            final_est_post=int(current_rating+K*(S-E)+B)
            # avg_opp=sum(opponent_list)/len(opponent_list)
            # post_est=(N*int(current_rating)+sum(opponent_list)+(2*n_win-tour_rounds)*400)/(N+tour_rounds)

            # st.write(avg_opp,post_est,tour_rounds)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f'Winning expectation: :orange[{round(E,2)}    ] ')
                if B>0:
                    st.write(f'Expected bonus points: :orange[{int(B)}    ] ')
            with col2:    
                norm_dict=get_norm(opponent_list,n_win)
                max_norm=0
                for k, t in norm_dict.items():
                    
                    if t=='yes' and max_norm <k:
                        max_norm=k
                    
                if max_norm>0:
                    st.write(f'Expected norm {max_norm}: :orange[{norm_dict[max_norm]}]')

            
            
            if final_est_post > current_rating:
                st.header(f'Your estimated post tournament rating is :green[{final_est_post} ], increased by :green[{final_est_post-current_rating}    ] ')
                # st.header(f'You may increase your rating by  :green[{final_est_post-current_rating}    ] ')
            else:
                st.header(f'Your estimated post tournament rating is :orange[{final_est_post}], dropped by :orange[{final_est_post-current_rating}     ] ')


            


        st.divider() 


            
