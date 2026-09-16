from datetime import datetime
from pprint import pprint
import requests
import pandas as pd

current_date = datetime.now()
current_date_str = current_date.strftime("%Y-%m-%d")

date = current_date_str

base_link = "https://api.ibb.gov.tr/ispark/Park"

def bulk_load_from_API(link=base_link):
        
        availability_response = requests.get(link)
        pprint(availability_response)
        #pprint(link)

        if availability_response.status_code == 200:
            df_car_park_raw_data = pd.read_json(link)
            pprint(link)
        
            return df_car_park_raw_data

        return availability_response


def detailed_load_from_API(link):
        availability_response = requests.get(link)
        pprint(availability_response)
        #pprint(link)

        if availability_response.status_code == 200:
            df_car_park_detailed_data = pd.read_json(link)
            pprint(link)
        
            return df_car_park_detailed_data

        return availability_response
      

