import mysql.connector
import  pandas as pd
import streamlit as st

def connect_to_database():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            database="movits"
        )
        cursor = mydb.cursor()
        
        return mydb, cursor

    except mysql.connector.Error as error:
        print(f"Error connecting to the database: {error}")
        return None, None

mydb, cursor =connect_to_database()
def check_database_state(mydb):
    if not mydb.is_connected():
        mydb.connect()
def get_column_names(cursor):
    return [desc[0] for desc in cursor.description]
def Add_column():
    # Check the state of the database
    check_database_state(mydb)
    cursor = mydb.cursor()
    query = "SELECT historique_passage_filtrer.*, \
             HOUR(historique_passage_filtrer.Heure_passage) AS hour, \
             DAY(historique_passage_filtrer.Heure_passage) AS day, \
             MONTH(historique_passage_filtrer.Heure_passage) AS month, \
             MINUTE(historique_passage_filtrer.Heure_passage) AS minute, \
             CONCAT(DATE(historique_passage_filtrer.Heure_passage), ' ', \
             LPAD(HOUR(historique_passage_filtrer.Heure_passage), 2, '0'), ':', \
             LPAD(MINUTE(historique_passage_filtrer.Heure_passage), 2, '0')) AS formatted_datetime, \
             DATE(historique_passage_filtrer.Heure_passage) AS new_date \
             FROM historique_passage_filtrer "
            #JOIN historique_passage ON vehicles.id = historique_passage.ID_Vehicle"
    
    cursor.execute(query)
    column_names = get_column_names(cursor)
    merged_data = [column_names] + cursor.fetchall()

    Merged_Vehicles_Historique_passage = pd.DataFrame(merged_data[1:], columns=merged_data[0])

    Merged_Vehicles_Historique_passage["class"].replace({"SEDAN": "C2", "TRUCK": "C3", "VEHICLE_UNCLASSED": "C1"}, inplace=True)
    Merged_Vehicles_Historique_passage.rename(columns={"class": "classe"}, inplace=True)
    return Merged_Vehicles_Historique_passage
def filter_data1(data, start_date):
    filtered_data_start = set()
    for index, row in data.iterrows():
        date = row['new_date']  # Access the date column (fifth element)
        if date==start_date:
            hour = row['hour']  # Access the hour column (first element)
            minute = row['minute']  # Access the minute column (fourth element)
            formatted_time = f"{hour:02d}:{minute:02d}"
            filtered_data_start.add(formatted_time) 
    if filtered_data_start is not None:
        list_min = sorted(filtered_data_start, reverse=False)
        return list(list_min)
    else:
        return list(filtered_data_start)
     
def filter_data2(data,end_date):
    filtered_data_end = set()
    for index, row in data.iterrows():
        date = row['new_date'] 
        # Access the date column (fifth element)      
        if date==end_date:
            hour = row['hour']  # Access the hour column (first element)
            minute = row['minute']  # Access the minute column (fourth element)
            formatted_time = f"{hour:02d}:{minute:02d}"
            filtered_data_end.add(formatted_time)
    if filtered_data_end is not None:
        list_max = sorted(filtered_data_end, reverse=True)
        return list(list_max)
    else:
        return list(filtered_data_end)
def zones():
    check_database_state(mydb)
    cursor = mydb.cursor()
    query="SELECT *FROM zones ORDER BY ID_zone ASC"
    cursor.execute(query)
    column_names = get_column_names(cursor)
    merged_df = [column_names] + cursor.fetchall()
    zones = pd.DataFrame(merged_df[1:], columns=merged_df[0])
    return zones

def Merged_Vehicles_alertes():
    check_database_state(mydb)
    cursor = mydb.cursor()
    query = "SELECT vehicles.id_v AS vehicle_id, vehicles.plaque_immatricule,\
    HOUR(alertes_filtrer.date_) AS hour,\
    MINUTE(alertes_filtrer.date_) AS minute, \
    vehicles.en_infration, alertes_filtrer.id_v, alertes_filtrer.ID_alertes, alertes_filtrer.Description, alertes_filtrer.Checked,\
    alertes_filtrer.camera, alertes_filtrer.chemin, alertes_filtrer.date_, CONCAT(DATE_FORMAT(alertes_filtrer.date_, '%Y-%m-%d %H:%i')) AS formatted_datetime, \
    DATE(alertes_filtrer.date_) AS new_date FROM vehicles JOIN alertes_filtrer ON vehicles.id_v = alertes_filtrer.id_v"
    cursor.execute(query)
    column_names = get_column_names(cursor)
    merged_df = [column_names] + cursor.fetchall()
    Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])
    Merged_Vehicles_alertes["Description"].replace({"stop": "Infraction véhicule"}, inplace=True)
    #Merged_Vehicles_alertes = Merged_Vehicles_alertes.loc[:, ~Merged_Vehicles_alertes.columns.duplicated()]
    Merged_Vehicles_alertes = Merged_Vehicles_alertes.loc[:, ~Merged_Vehicles_alertes.columns.duplicated()]
    if 'id_v' in Merged_Vehicles_alertes.columns:
        Merged_Vehicles_alertes = Merged_Vehicles_alertes.drop_duplicates(subset=['id_v'], keep='first')
    
    return Merged_Vehicles_alertes

def user(username,password):
    check_database_state(mydb)
    cursor=mydb.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result
   