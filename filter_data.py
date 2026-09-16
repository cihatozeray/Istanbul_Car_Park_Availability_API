import sqlalchemy
#from sqlalchemy import create_engine
import psycopg2 as pg
from psycopg2 import sql
from datetime import datetime
import pandas as pd
import json

current_date = datetime.now()
current_month_str = current_date.strftime("%Y_%m")

table_name_base = "Ispark_Car_Park_Info_General"

#importing credentials
with open("credentials.json", "r") as local_cred_file:
    postgresql_credentials = json.load(local_cred_file)

schema = "Ispark_Availability_Study"
database = "car_park_Istanbul"


def get_district_names_from_localdb ():
    try:
        conn = pg.connect(
            host=postgresql_credentials["host"],
            database=database,
            user=postgresql_credentials["username"],
            password=postgresql_credentials["password"],
            port=postgresql_credentials["port"],
        )

        cur = conn.cursor()
        print('connected successfully')

        table_name = table_name_base + "_" + current_month_str
        
        query_for_district = sql.SQL("select distinct(district) from {}.{};").format(sql.Identifier(schema),
                                                                                     sql.Identifier(table_name))
        print(query_for_district)
        cur.execute(query_for_district)

        district_list = cur.fetchall()

        cur.close()
        conn.close()

        print(district_list)
        return district_list

    except Exception as e:
        print(e)


def get_data_from_localdb (columns, filtered_column, filter_condition):
    try:
        conn = pg.connect(
            host=postgresql_credentials["host"],
            database=database,
            user=postgresql_credentials["username"],
            password=postgresql_credentials["password"],
            port=postgresql_credentials["port"],
        )

        cur = conn.cursor()
        print('connected successfully')

        table_name = table_name_base + "_" + current_month_str
        #column_names_sql = ",".join(columns)
        columns = [sql.Identifier(i) for i in columns]
        fields = sql.SQL(",").join(columns)
        query_for_district = sql.SQL("select {} from {}.{} where {} like {};").format(fields,
                                                                                            sql.Identifier(schema),
                                                                                            sql.Identifier(table_name),
                                                                                            sql.Identifier(filtered_column),
                                                                                            sql.Literal(filter_condition))
        print(query_for_district)
        cur.execute(query_for_district)

        district_list = cur.fetchall()

        cur.close()
        conn.close()

        print(district_list)
        return district_list

    except Exception as e:
        print(e)