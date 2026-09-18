import streamlit as st
import get_raw_data_IMM_api
import Ispark_data_into_postgres
import filter_data
from datetime import datetime
from pprint import pprint
import requests
import pandas as pd
import matplotlib.pyplot as plt

base_link = "https://api.ibb.gov.tr/ispark/Park"
# Istanbul Metropolitan Municipality Open Data Portal Api is used.
# Lisans will be added
#df_car_park_data = get_raw_data_IMM_api.bulk_load_from_API(base_link) #downloads information related to all Ispark
#df_car_park_data.drop(columns="emptyCapacity", inplace=True) 
#empty capacity information is refreshed near real time, so it is removed from the table that will be used for reference


#Park_ID = 359
#detailed_link = base_link + "Detay?id=" + str(Park_ID)

def detailed_link_creator(Park_ID):
    detailed_link = base_link + "Detay?id=" + str(Park_ID)
    return detailed_link

#link_template = "https://api.ibb.gov.tr/ispark/ParkDetay?id=(PARKID)"
#pprint(detailed_link)

#df_detailed_park_data = get_raw_data_IMM_api.detailed_load_from_API(detailed_link)

#Ispark_data_into_postgres.create_postgres_table(df_car_park_data)


district_list = filter_data.get_district_names_from_localdb()
district_list = [i[0] for i in district_list]
pprint(district_list)

st.title("İsPark Doluluk")

district = st.selectbox(label="İlçe Seçiniz", options=district_list)
#district = "ÜSKÜDAR"


def get_park_IDs_and_names():
    park_IDs_and_names = filter_data.get_data_from_localdb(columns= ["parkID", "parkName"], filtered_column="district", filter_condition=district)
    #Park_ID_list = [str(i[0]) for i in park_IDs_and_names]
    #Park_names_list = [i[1] for i in park_IDs_and_names]
    dict_park_IDs_and_names = {i[1]:i[0] for i in park_IDs_and_names}
    #pprint(Park_ID_list)
    #pprint(Park_names_list)
    #return [Park_ID_list, Park_names_list]
    return dict_park_IDs_and_names

dict_park_IDs_and_names = get_park_IDs_and_names()

#park_IDs = park_IDs_and_names()[0]
#park_names = park_IDs_and_names()[1]

#pprint(park_IDs)
#pprint(park_names)
pprint(dict_park_IDs_and_names)

#str_park_IDs_for_API = ",".join(park_IDs)
#detailed_link = base_link + "Detay?id=" + str_park_IDs_for_API

#park_names = [i for i in dict_park_IDs_and_names.keys]
carpark = st.selectbox(label="Otopark Seçiniz", options=list(dict_park_IDs_and_names.keys()))

park_ID = dict_park_IDs_and_names[carpark]

detailed_link = detailed_link_creator(park_ID)

df_detailed_park_data = get_raw_data_IMM_api.detailed_load_from_API(detailed_link)

#st.write(park_ID)

#st.dataframe(df_detailed_park_data)

capacity = df_detailed_park_data["capacity"][0].item()
empty_capacity = df_detailed_park_data["emptyCapacity"][0].item()
occupied = capacity - empty_capacity

pie_chart_sizes = [capacity, occupied, empty_capacity]
labels = ['', 'DOLU:' + str(occupied), 'BOŞ:' + str(empty_capacity)]
colors = ['white', '#ff6f60', '#cdeee1']
#colors = ['white', '#D3D3D3', '#2a3c54']
explode = [0, 0.05, 0]

fig, ax = plt.subplots()
ax.pie(pie_chart_sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        counterclock=False)

#st.pyplot(fig)

str_update_date = df_detailed_park_data["updateDate"][0]

update_date_api = datetime.strptime(str_update_date, "%d.%m.%Y %H:%M:%S")
now_time = datetime.now()
time_difference = now_time - update_date_api

#st.write(update_date_api)
#st.write(time_difference)

def timedelta_to_fractions(timediff):
    timer_in_sec = timediff.total_seconds()
    days = timer_in_sec//86400
    hours = timer_in_sec//3600
    mins = (timer_in_sec//60)%60
    seconds = timer_in_sec%60

    return [int(days), int(hours), int(mins), int(seconds)]

time_diff_fractions = timedelta_to_fractions(time_difference)
time_diff_fractions_str = [str(i) for i in time_diff_fractions]
time_labels = ["gün", "saat", "dakika", "saniye"]

def time_diff_line_maker(time_diff_fractions_str, time_labels):
    time_board = "" 
    for i in range(4): 
        if time_diff_fractions[i] != 0:
            time_board = time_board + time_diff_fractions_str[i] + " " + time_labels[i] + ", " 

    time_board = time_board[:-2] + " öncesi:"

    if time_diff_fractions == [0,0,0,0]:
        time_board = "Güncel:"
        
    return time_board

time_diff_line_str = time_diff_line_maker(time_diff_fractions_str, time_labels)


st.write(time_diff_line_str)
st.pyplot(fig)

#








