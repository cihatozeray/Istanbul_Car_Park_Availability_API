from sqlalchemy import create_engine
from datetime import datetime
import json

current_date = datetime.now()
current_month_str = current_date.strftime("%Y_%m")

table_name_base = "Ispark_Car_Park_Info_General"

#importing credentials
with open("credentials.json", "r") as local_cred_file:
    postgresql_credentials = json.load(local_cred_file)

username = postgresql_credentials["username"]
password = postgresql_credentials["password"]
host = postgresql_credentials["host"]
port = postgresql_credentials["port"]
schema = "Ispark_Availability_Study"
database = "car_park_Istanbul"



def create_postgres_table( dataframe,
                           database=database,
                           schema=schema, 
                           table_name_base=table_name_base,
                           username=username,
                           password=password,
                           date=current_month_str):

    table_name = table_name_base + "_" + date

    url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    engine = create_engine(url)

    dataframe.to_sql( name=table_name, 
                      con=engine,
                      schema=schema,
                      if_exists='replace')

    #return table properties here for later!!
    print("executed!")