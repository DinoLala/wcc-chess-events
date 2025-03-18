import requests
from bs4 import BeautifulSoup
import pandas as pd

class process_html(object):
    def read_text(self, html_file):
        text_file=open(html_file,"r")
        html_str=text_file.read()
        text_file.close()
        return html_str
    def process_tb(self, html_str):
        # soup=BeautifulSoup(html_str,'html.parse')
        soup = BeautifulSoup(html_str, "lxml")
        tables=[
            [
                [
                    td.get_text(strip=True) for td in tr.find_all('td')
                ]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]
        if tables[-1]==[]:
            tables.pop(-1)
        df=pd.DataFrame(tables[-1][:])
        # df=df.rename(columns=df.iloc[0])
       
        df=df.iloc[1:,:]
        return df
    def get_norm_stat(self, html_str):

        soup = BeautifulSoup(html_str, "lxml")
        soup.find_all('table')
        tables=[
            [
                [
                    td.get_text(strip=True) for td in tr.find_all('td')
                ]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]
        # tables
        for t in tables:
            if t[0]==['Norms Earned Since 1991']:
                norm_tb=[tb for tb in t if len(tb)==3]

        norm_df=pd.DataFrame(norm_tb, columns=['event','section','level'])
        norm_df_sum=norm_df['level'].value_counts().reset_index()
        # norm_tb=pd.DataFrame()
        print(norm_df_sum)
        # if tables[-1]==[]:
        #     tables.pop(-1)
        # df=pd.DataFrame(tables[-1][:])
        # print(df)
        return norm_df_sum
# h=process_html()
def get_player(h, uscf_id):

    # ='30305579'
    my_url='https://www.uschess.org/msa/MbrDtlMain.php?'+uscf_id

    re = requests.get(my_url)
    dict_out={}
    # print(re.text)
    text_file=re.text
    # text_file=[c.lower() for c in text_file]
    html_tables=h.process_tb(text_file)
    col_index=html_tables[0]


    name_find=text_file.split('<b>')
    Name=[c for c in name_find if uscf_id in c][0].split('</b>')[0]
    Name=Name.split(':')[-1]
    
    State=html_tables.loc[html_tables[0]=='State',:][1].reset_index()[1][0]

    Gender=html_tables.loc[html_tables[0]=='Gender',:][1].reset_index()[1][0]
    try:
        Junior_Ranking=html_tables.loc[html_tables[0]=='Junior Ranking',:][2].reset_index()[2][0]
    except:
        Junior_Ranking='none'
    try:
        Over_Ranking=html_tables.loc[html_tables[0]=='Overall Ranking',:][2].reset_index()[2][0]
    except:
        Over_Ranking='none'

    
    try:
        # state_rank='State Ranking ('+str(State)+')'
        state_rank=[c for c in col_index if 'State Ranking' in c  and 'National' not in c][0]
        State_Ranking=html_tables.loc[html_tables[0]==state_rank,:][2].reset_index()[2][0]
    except:
        State_Ranking='none'

    try:
        title=[c for c in col_index if 'US Chess Titles Earned' in c ][0]
        # title

        title_name=html_tables.loc[html_tables[0]==title,:][1].reset_index()[1][0]
    except:
        title_name='none'

    try:
        current_rating=[c for c in col_index if 'Regular Rating' in c ][0]
        # current_rating

        current_rate=html_tables.loc[html_tables[0]==current_rating,:][1].reset_index()[1][0]
        nextmonth_rate=html_tables.loc[html_tables[0]==current_rating,:][2].reset_index()[2][0][:4]
        if len(current_rate)>4 and "Unrate" not in current_rate:
            current_rate=current_rate[:4]
        # current_rate
    except:
        current_rate='Unrate'  
        nextmonth_rate='Unrate'  
    



    title_name
    dict_out['Name']=Name
    dict_out['State']=State
    dict_out['Gender']=Gender
    dict_out['Junior_Ranking']=Junior_Ranking
    dict_out['Over_Ranking']=Over_Ranking
    dict_out['State_Ranking']=State_Ranking
    dict_out['title_name']=title_name
    dict_out['current_rating']=current_rate
    dict_out['nextmonth_rate']=nextmonth_rate

    return dict_out

def get_tournaments(h,uscf_id):
    my_url='https://www.uschess.org/msa/MbrDtlTnmtHst.php?'+uscf_id
    re = requests.get(my_url)
    # print(re.text)
    text_file=re.text
    html_tables=h.process_tb(text_file)
    if len(html_tables) <=50:
        html_tables.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
    else: 
        html_tables=html_tables.iloc[1:,:]
        
        html_tables.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
        
    html_tables['End_event_date'] =html_tables['End_event_date'].apply(lambda x: x[:10])
    # try:
    #     my_url='https://www.uschess.org/msa/MbrDtlTnmtHst.php?'+uscf_id+'.2'
    #     re = requests.get(my_url)
    #     # print(re.text)
    #     text_file=re.text
    #     html_tables2=h.process_tb(text_file)
    #     if len(html_tables2) <=50:
    #         html_tables2.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
    #     else: 
    #         html_tables2=html_tables2.iloc[1:,:]

    #         html_tables2.columns=['End_event_date','Event_name','reg Rtg Before/After','Quick Rtg Before/After','Bliz Rtg Before/After']
    #         html_tables2['End_event_date'] =html_tables2['End_event_date'].apply(lambda x: x[:10])

    #     html_tables=pd.concat([html_tables,html_tables2], axis=0)
    # except:
    #     pass
    return html_tables
    

def get_all_games(uscf_id):
    # my_url='https://www.uschess.org/datapage/gamestats.php?memid=30581110&ptype=G&rs=R&dkey=1300&drill=G'
    rate_list=['UNR','100','200','300','400','500','600','700','800','900',
            '1000','1100','1200','1300','1400','1500'
            ,'1600','1700','1800','1900','2000','2100','2200','2300','2400','2500','2600','2700','2800']
    df_all_games=pd.DataFrame()
    for r in rate_list:
    # for r in ['1700']:
        # print(r)
        my_url='https://www.uschess.org/datapage/gamestats.php?memid='+uscf_id+'&ptype=G&rs=R&dkey='+r+'&drill=G'
        print(my_url)
        try:
            re = requests.get(my_url)
            # print(re.text)
            text_file=re.text

            soup = BeautifulSoup(text_file, "lxml")
            tables=[
                [
                    [
                        td.get_text(strip=True) for td in tr.find_all('td')
                    ]
                    for tr in table.find_all('tr')
                ]
                for table in soup.find_all('table')
            ]
            if tables[-1]==[]:
                tables.pop(-1)
            df=pd.DataFrame(tables[-3][:])
            df=df.rename(columns=df.iloc[0])
            
            df=df.dropna()
            # print('============',df)

            # print(df)
            df.columns=['Event',	'Section',	'round','color','Oponent USCF'	,'Oponent name','Rating','Result']
            
            
            df_all_games=pd.concat([df_all_games,df], axis=0)
            # print('============',df)
        except:
            # print('not found', r)
            pass
    return df_all_games

def get_norm_summary(h,uscf_id):
    norm_url='https://www.uschess.org/datapage/norms-list.php?'+uscf_id
    re = requests.get(norm_url)
    text_file=re.text
    try:
        norm_df=h.get_norm_stat(text_file)
    except:
        norm_df=pd.DataFrame()

    return norm_df

def get_norm(opponent_list,n_win):
    norm_dict={}
    if len(opponent_list) <4:
        return norm_dict
    else:
        for c in [1200, 1400,1600,1800]:
            C_t=0
            for p in opponent_list:
                del_i=c-p
                if del_i <= -400:
                    c_i=0
                elif del_i <=0 and del_i >-400:
                    c_i=.5+del_i/800
                elif del_i >0 and del_i <=200:
                    c_i=.5+del_i/400
                else:
                    c_i=1
                C_t=C_t+c_i
            if n_win- C_t>1:
                norm_dict[c]='yes'
            else:
                norm_dict[c]='no'
        return norm_dict
