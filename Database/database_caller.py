# import  Database.Dataset 
# import  pandas as pd
# import streamlit as st
# mydb, cursor = Database.Dataset.connect_to_database()
# def check_database_state(mydb):
#     if not mydb.is_connected():
#         mydb.connect()
# def get_column_names(cursor):
#     return [desc[0] for desc in cursor.description]

# # def Historique_passage():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT * FROM Historique_passage"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     df_historique_passage = [column_names] + cursor.fetchall()
# #     df_historique_passage = pd.DataFrame(df_historique_passage[1:], columns=df_historique_passage[0])
# #     return df_historique_passage
# #     # Fetch the query results
# # def Vehicles():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT * FROM vehicles"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     df_vehicles = [column_names] + cursor.fetchall()
# #     df_vehicles = pd.DataFrame(df_vehicles[1:], columns=df_vehicles[0])
# #     return df_vehicles
# # def Merged_Vehicles_Historique_passage():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM vehicles JOIN historique_passage ON vehicles.id =historique_passage.ID_Vehicle"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     Merged_Vehicles_Historique_passage = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return Merged_Vehicles_Historique_passage

# def Add_column():
#     # Check the state of the database
#     check_database_state(mydb)
#     cursor = mydb.cursor()
#     query = "SELECT historique_passage_filtrer.*, \
#              HOUR(historique_passage_filtrer.Heure_passage) AS hour, \
#              DAY(historique_passage_filtrer.Heure_passage) AS day, \
#              MONTH(historique_passage_filtrer.Heure_passage) AS month, \
#              MINUTE(historique_passage_filtrer.Heure_passage) AS minute, \
#              CONCAT(DATE(historique_passage_filtrer.Heure_passage), ' ', \
#              LPAD(HOUR(historique_passage_filtrer.Heure_passage), 2, '0'), ':', \
#              LPAD(MINUTE(historique_passage_filtrer.Heure_passage), 2, '0')) AS formatted_datetime, \
#              DATE(historique_passage_filtrer.Heure_passage) AS new_date \
#              FROM historique_passage_filtrer "
#             #JOIN historique_passage ON vehicles.id = historique_passage.ID_Vehicle"
    
#     cursor.execute(query)
#     column_names = get_column_names(cursor)
#     merged_data = [column_names] + cursor.fetchall()

#     Merged_Vehicles_Historique_passage = pd.DataFrame(merged_data[1:], columns=merged_data[0])

#     Merged_Vehicles_Historique_passage["class"].replace({"SEDAN": "C2", "TRUCK": "C3", "VEHICLE_UNCLASSED": "C1"}, inplace=True)
#     Merged_Vehicles_Historique_passage.rename(columns={"class": "classe"}, inplace=True)
#     return Merged_Vehicles_Historique_passage
# def filter_data1(data, start_date):
#     filtered_data_start = set()
#     for index, row in data.iterrows():
#         date = row['new_date']  # Access the date column (fifth element)
#         if date==start_date:
#             hour = row['hour']  # Access the hour column (first element)
#             minute = row['minute']  # Access the minute column (fourth element)
#             formatted_time = f"{hour:02d}:{minute:02d}"
#             filtered_data_start.add(formatted_time) 
#     if filtered_data_start is not None:
#         list_min = sorted(filtered_data_start, reverse=False)
#         return list(list_min)
#     else:
#         return list(filtered_data_start)
     
# def filter_data2(data,end_date):
#     filtered_data_end = set()
#     for index, row in data.iterrows():
#         date = row['new_date'] 
#         # Access the date column (fifth element)      
#         if date==end_date:
#             hour = row['hour']  # Access the hour column (first element)
#             minute = row['minute']  # Access the minute column (fourth element)
#             formatted_time = f"{hour:02d}:{minute:02d}"
#             filtered_data_end.add(formatted_time)
#     if filtered_data_end is not None:
#         list_max = sorted(filtered_data_end, reverse=True)
#         return list(list_max)
#     else:
#         return list(filtered_data_end)
# # @st.cache_data
# # def Merged_Vehicles_Historique_passage_alertes(Sens,classe):
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT vehicles.id AS '(ID) Vehicles', historique_passage.Heure_passage AS 'Historique Passage', \
# #              historique_passage.id AS '(ID) Historique de passage', vehicles.classe AS 'Classe', \
# #              vehicles.en_infration AS 'En Infration', historique_passage.sens AS 'Sens', \
# #              alertes.camera AS 'Camera' \
# #              LPAD(MINUTE(historique_passage.Heure_passage), 2, '0')) AS formatted_datetime, \
# #              FROM vehicles \
# #              JOIN historique_passage ON vehicles.id = historique_passage.ID_Vehicle \
# #              JOIN alertes ON vehicles.id = alertes.id_v \
# #              WHERE historique_passage.sens = %s AND vehicles.classe= %s"
# #     cursor.execute(query, (Sens,classe))
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     merged_df = pd.DataFrame(merged_df[1:], columns=merged_df[0])
# #     return merged_df
# # @st.cache_data
# # def Merged_Vehicles_Historique_passage_alertes_all():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT vehicles.id AS '(ID) Vehicles', historique_passage.Heure_passage AS 'Historique Passage', \
# #              vehicles.classe AS 'Classe', \
# #              vehicles.en_infration AS 'En Infration', historique_passage.sens AS 'Sens', \
# #              LPAD(MINUTE(historique_passage.Heure_passage), 2, '0')) AS formatted_datetime, \
# #              FROM vehicles \
# #              JOIN historique_passage ON vehicles.id = historique_passage.ID_Vehicle"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     merged_df = pd.DataFrame(merged_df[1:], columns=merged_df[0])
# #     return merged_df
# # #alertes-table+Vehicles+table
# # def Merged_Vehicles_alertes():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM vehicles JOIN alertes ON vehicles.id =alertes.id_v"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return Merged_Vehicles_alertes
# # def alertes():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM alertes"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return alertes

# def zones():
#     check_database_state(mydb)
#     cursor = mydb.cursor()
#     query="SELECT *FROM zones ORDER BY ID_zone ASC"
#     cursor.execute(query)
#     column_names = get_column_names(cursor)
#     merged_df = [column_names] + cursor.fetchall()
#     zones = pd.DataFrame(merged_df[1:], columns=merged_df[0])
#     return zones

# def Merged_Vehicles_alertes():
#     check_database_state(mydb)
#     cursor = mydb.cursor()
#     query = "SELECT vehicles.id_v AS vehicle_id, vehicles.plaque_immatricule,\
#     HOUR(alertes_filtrer.date_) AS hour,\
#     MINUTE(alertes_filtrer.date_) AS minute, \
#     vehicles.en_infration, alertes_filtrer.id_v, alertes_filtrer.ID_alertes, alertes_filtrer.Description, alertes_filtrer.Checked,\
#     alertes_filtrer.camera, alertes_filtrer.chemin, alertes_filtrer.date_, CONCAT(DATE_FORMAT(alertes_filtrer.date_, '%Y-%m-%d %H:%i')) AS formatted_datetime, \
#     DATE(alertes_filtrer.date_) AS new_date FROM vehicles JOIN alertes_filtrer ON vehicles.id_v = alertes_filtrer.id_v"
#     cursor.execute(query)
#     column_names = get_column_names(cursor)
#     merged_df = [column_names] + cursor.fetchall()
#     Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])
#     Merged_Vehicles_alertes["Description"].replace({"stop": "Infraction véhicule"}, inplace=True)
#     #Merged_Vehicles_alertes = Merged_Vehicles_alertes.loc[:, ~Merged_Vehicles_alertes.columns.duplicated()]
#     Merged_Vehicles_alertes = Merged_Vehicles_alertes.loc[:, ~Merged_Vehicles_alertes.columns.duplicated()]
#     if 'id_v' in Merged_Vehicles_alertes.columns:
#         Merged_Vehicles_alertes = Merged_Vehicles_alertes.drop_duplicates(subset=['id_v'], keep='first')
    
#     return Merged_Vehicles_alertes

# def user(username,password):
#     check_database_state(mydb)
#     cursor=mydb.cursor()
#     query = "SELECT * FROM users WHERE username = %s AND password = %s"
#     cursor.execute(query, (username, password))
#     result = cursor.fetchone()
#     return result
   
# # def update_zones(df):

# #     check_database_state(mydb)
# #     cursor=mydb.cursor()
# #     for index, row in df.iterrows():
# #         id_zone = row['ID_zone']
# #         p1_x = row['P1_X']
# #         p1_y = row['P1_Y']
# #         p2_x = row['P2_X']
# #         p2_y = row['P2_Y']
# #         label = row['type']
    
# #     # Execute the necessary SQL statement to update the database
# #     # Modify the SQL statement based on your database structure and table name
# #         cursor.execute("UPDATE zones SET P1_X = %s, P1_Y = %s, P2_X = %s, P2_Y = %s, type = %s WHERE ID_zone = %s", (p1_x, p1_y, p2_x, p2_y, label, id_zone))
# #     mydb.commit()
        


# # def insert_zone(df):
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()

# #     # Retrieve the existing ID_zone values from the database
# #     existing_id_zones = set()
# #     query_existing_zones = "SELECT ID_zone FROM zones"
# #     cursor.execute(query_existing_zones)
# #     existing_zones = cursor.fetchall()
# #     existing_id_zones.update(zone[0] for zone in existing_zones)
# #     # Create a set to store the ID_zone values from the DataFrame
# #     df_id_zones = set(df['ID_zone'])

# #     # Find the ID_zone values that exist in the database but not in the DataFrame
# #     delete_id_zones = existing_id_zones - df_id_zones

# #     # Delete the rows with the corresponding ID_zone values
# #     if delete_id_zones:
# #         query_delete_zones = "DELETE FROM zones WHERE ID_zone IN (%s)"
# #         delete_params = ",".join(str(zone) for zone in delete_id_zones)
# #         cursor.execute(query_delete_zones % delete_params)
# #     for index, row in df.iterrows():
# #         id_zone = row['ID_zone']

# #         # Check if the ID_zone already exists in the database
# #         if id_zone not in existing_id_zones:
# #             p1_x = row['P1_X']
# #             p1_y = row['P1_Y']
# #             p2_x = row['P2_X']
# #             p2_y = row['P2_Y']
# #             label = row['type']
# #             query = "INSERT INTO zones (ID_zone, P1_X, P1_Y, P2_X, P2_Y, type) VALUES (%s, %s, %s, %s, %s, %s)"
# #             cursor.execute(query, (id_zone, p1_x, p1_y, p2_x, p2_y, label))

# #     mydb.commit()
# # def max_zone():
# #         # Reverse the type_mapping dictionary to map integers to labels
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT MAX(ID_zone) FROM zones"
# #     cursor.execute(query)

# #     # Fetch the result
# #     result = cursor.fetchone()

# #     # Close the cursor and database connection
# #     cursor.close()
# #     mydb.close()

# #     # Return the maximum id_zone value
# #     max_id_zone = result[0] if result[0] is not None else 0
# #     return max_id_zone
# anomalie=Merged_Vehicles_alertes()

#     # alertes_vehicles_data=Merged_Vehicles_alertes()
# last_date = Add_column()['new_date'].max()
# last_date_alertes=Merged_Vehicles_alertes()['new_date'].max()
# data=Add_column()

# # print(data)
# # data_alertes=alertes()
# # zones_data=zones()
# # import  Database.Dataset 
# # import  pandas as pd
# # import streamlit as st

# # mydb, cursor = Database.Dataset.connect_to_database()
# # def check_database_state(mydb):
# #     if not mydb.is_connected():
# #         mydb.connect()
# # def get_column_names(cursor):
# #     return [desc[0] for desc in cursor.description]
# # def Historique_passage():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT * FROM historique_passage"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     df_historique_passage = [column_names] + cursor.fetchall()
# #     df_historique_passage = pd.DataFrame(df_historique_passage[1:], columns=df_historique_passage[0])
# #     return df_historique_passage
# #     # Fetch the query results
# # def Vehicles():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT * FROM vehicles"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     df_vehicles = [column_names] + cursor.fetchall()
# #     df_vehicles = pd.DataFrame(df_vehicles[1:], columns=df_vehicles[0])
# #     return df_vehicles
# # def Merged_Vehicles_Historique_passage():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM vehicles JOIN historique_passage ON vehicles.id_v =historique_passage.ID_vehicle"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     Merged_Vehicles_Historique_passage = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return Merged_Vehicles_Historique_passage
# # def Add_column():
# #     # Check the state of the database
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT vehicles.*, historique_passage.*, \
# #              HOUR(historique_passage.Heure_passage) AS hour, \
# #              DAY(historique_passage.Heure_passage) AS day, \
# #              MONTH(historique_passage.Heure_passage) AS month, \
# #              MINUTE(historique_passage.Heure_passage) AS minute, \
# #              CONCAT(DATE(historique_passage.Heure_passage), ' ', \
# #              LPAD(HOUR(historique_passage.Heure_passage), 2, '0'), ':', \
# #              LPAD(MINUTE(historique_passage.Heure_passage), 2, '0')) AS formatted_datetime, \
# #              DATE(historique_passage.Heure_passage) AS new_date \
# #              FROM vehicles \
# #              JOIN historique_passage ON vehicles.id_v = historique_passage.ID_vehicle"
    
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_data = [column_names] + cursor.fetchall()

# #     Merged_Vehicles_Historique_passage = pd.DataFrame(merged_data[1:], columns=merged_data[0])

    
# #     return Merged_Vehicles_Historique_passage
# # def filter_data1(data, start_date):
# #     filtered_data_start = set()
# #     for index, row in data.iterrows():
# #         date = row['new_date']  # Access the date column (fifth element)
# #         if date==start_date:
# #             hour = row['hour']  # Access the hour column (first element)
# #             minute = row['minute']  # Access the minute column (fourth element)
# #             formatted_time = f"{hour:02d}:{minute:02d}"
# #             filtered_data_start.add(formatted_time) 
# #     if filtered_data_start is not None:
# #         list_min = sorted(filtered_data_start, reverse=False)
# #         return list(list_min)
# #     else:
# #         return list(filtered_data_start)
     
# # def filter_data2(data,end_date):
# #     filtered_data_end = set()
# #     for index, row in data.iterrows():
# #         date = row['new_date'] 
# #         if date==end_date:
# #             hour = row['hour']  # Access the hour column (first element)
# #             minute = row['minute']  # Access the minute column (fourth element)
# #             formatted_time = f"{hour:02d}:{minute:02d}"
# #             filtered_data_end.add(formatted_time)
# #     if filtered_data_end is not None:
# #         list_max = sorted(filtered_data_end, reverse=True)
# #         return list(list_max)
# #     else:
# #         return list(filtered_data_end)
# # # @st.cache_data
# # # def Merged_Vehicles_Historique_passage_alertes(Sens,classe):
# # #     check_database_state(mydb)
# # #     cursor = mydb.cursor()
# # #     query = "SELECT vehicles.id AS '(ID) Vehicles', historique_passage.Heure_passage AS 'Historique Passage', \
# # #              historique_passage.id AS '(ID) Historique de passage', vehicles.classe AS 'Classe', \
# # #              vehicles.en_infration AS 'En Infration', historique_passage.sens AS 'Sens', \
# # #              alertes.camera AS 'Camera' \
# # #              LPAD(MINUTE(historique_passage.Heure_passage), 2, '0')) AS formatted_datetime, \
# # #              FROM Vehicles \
# # #              JOIN historique_passage ON vehicles.id = historique_passage.ID_Vehicle \
# # #              JOIN alertes ON vehicles.id = alertes.ID_Vehicle \
# # #              WHERE historique_passage.sens = %s AND vehicles.classe= %s"
# # #     cursor.execute(query, (Sens,classe))
# # #     column_names = get_column_names(cursor)
# # #     merged_df = [column_names] + cursor.fetchall()
# # #     merged_df = pd.DataFrame(merged_df[1:], columns=merged_df[0])
# # #     return merged_df

# # def Merged_Vehicles_Historique_passage_alertes_all():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT vehicles.id_v AS '(ID) Vehicles', historique_passage.Heure_passage AS 'Historique Passage', \
# #              vehicles.classe AS 'Classe', \
# #              vehicles.en_infration AS 'En Infration', historique_passage.sens AS 'Sens', \
# #              LPAD(MINUTE(historique_passage.Heure_passage), 2, '0')) AS formatted_datetime, \
# #              FROM vehicles \
# #              JOIN historique_passage ON vehicles.id_v = historique_passage.ID_vehicle"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     merged_df = pd.DataFrame(merged_df[1:], columns=merged_df[0])
# #     return merged_df
# # # #alertes-table+Vehicles+table
# # # def Merged_Vehicles_alertes():
# # #     check_database_state(mydb)
# # #     cursor = mydb.cursor()
# # #     query="SELECT *FROM vehicles JOIN alertes ON vehicles.id_v =alertes.id_v"
# # #     cursor.execute(query)
# # #     column_names = get_column_names(cursor)
# # #     merged_df = [column_names] + cursor.fetchall()
# # #     Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# # #     return Merged_Vehicles_alertes
# # def alertes():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM alertes"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return alertes

# # def zones():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query="SELECT *FROM zones"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     zones = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return zones
# # def Merged_Vehicles_alertes():
# #     check_database_state(mydb)
# #     cursor = mydb.cursor()
# #     query = "SELECT *, CONCAT(DATE_FORMAT(alertes.date_, '%Y-%m-%d %H:%i')) AS formatted_datetime, DATE(alertes.date_) AS new_date FROM vehicles JOIN alertes ON vehicles.id_v = alertes.id_v"
# #     cursor.execute(query)
# #     column_names = get_column_names(cursor)
# #     merged_df = [column_names] + cursor.fetchall()
# #     Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])

# #     return Merged_Vehicles_alertes
# # anomalie=Merged_Vehicles_alertes()
# # alertes_vehicles_data=Merged_Vehicles_alertes()
# # last_date = Add_column()['new_date'].max()
# # data=Add_column()
# # data_alertes=alertes()
# # zones_data=zones()