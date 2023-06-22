import streamlit as st
import datetime
import streamlit.components.v1 as components

import plotly.express as px
import pandas as pd
import Database.database_caller
import plotly.graph_objs as go
import io
import anomalie_
import infraction_
from functions.chart_anomalie import chart_anomalie_infraction
def Anomaile():
    select=True
    if select:
        mydb, cursor =Database.Dataset.connect_to_database()
        def check_database_state(mydb):
            if not mydb.is_connected():
                mydb.connect()
        def get_column_names(cursor):
            return [desc[0] for desc in cursor.description]
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
    data=Merged_Vehicles_alertes()
    st.markdown('<style>' + open('./Style/anomalie.css').read() + '</style>', unsafe_allow_html=True)
    empty_col,col_display,empty_col1=st.columns([0.01,5,0.01])
    with col_display:
        col_min_date, col_max_date = st.columns([2, 2])

        if 'min_date1' not in st.session_state or 'max_date1' not in st.session_state:
            st.session_state.min_date1 = data['new_date'].max() #- datetime.timedelta(days=1)
            st.session_state.max_date1 = data['new_date'].max()

        min_date1 = st.session_state.min_date1
        max_date1 = st.session_state.max_date1

        min_date1 = col_min_date.date_input("Start Date", min_date1)
        max_date1 = col_max_date.date_input("End Date", max_date1)

        # with col_advance_filter:
        #     with col_advance_filter.expander("filtre avancé",False):

        #         option_date11=Database.database_caller.filter_data1(Database.database_caller.data,min_date1)
        #         option_date22=Database.database_caller.filter_data2(Database.database_caller.data,max_date1)
        #         time_start2=st.selectbox("Start Time",option_date11)
        #         time_end2=st.selectbox("End Time",option_date22)
        #         if time_start2 is not None:
        #             time_obj1 = datetime.datetime.strptime(time_start2, "%H:%M").time()  # Convert string to `datetime.time` object
        #             merged_datetime_formatted11 = datetime.datetime.combine(min_date1, time_obj1) 
        #         else:
        #             st.warning("This start date not exist")
        #         if time_end2 is not None:
        #                 time_obj2 = datetime.datetime.strptime(time_end2, "%H:%M").time()
        #                 merged_datetime_formatted22 = datetime.datetime.combine(max_date1, time_obj2)
        #         else:
        #                 st.warning("This end date not exist")
        #         button_filter=st.button("Filter ")
        #         if button_filter:
        #              Database.database_caller.data['formatted_datetime'] = pd.to_datetime(Database.database_caller.data['formatted_datetime'], format='%Y-%m-%d %H:%M')
        #              df = Database.database_caller.data[(Database.database_caller.data["formatted_datetime"]>= merged_datetime_formatted11)& (Database.database_caller.data["formatted_datetime"]<= merged_datetime_formatted22)] 
        #         else:
        #             df = Database.database_caller.data[(Database.database_caller.data["new_date"]>= min_date1)& (Database.database_caller.data["new_date"]<= max_date1)] #Need to add the handle of min value in hours
        col_space_chart_left,col_chart_1,col_space_chart_2_right=st.columns([0.01,1,0.01])

     
        with col_chart_1:
            pass

        #     df = Database.database_caller.anomalie[(Database.database_caller.anomalie["new_date"] >= min_date1) & (Database.database_caller.anomalie["new_date"] <= max_date1)] 
        #         # Convert 'Heure_passage' column to datetime format
        #     df['date_'] = pd.to_datetime(df['date_'])
            
        #     # Extract date component and assign it to 'Jour' column
        #     df['Jour'] = df['date_'].dt.strftime('%Y-%m-%d')
            
        #     # Extract time component and assign it to 'Date(min)' column
        #     df['Date(min)'] = df['date_'].dt.strftime('%H:%M')
        #     if max_date1 == min_date1:
        #                 df['Date(min)'] = pd.to_datetime(df['Date(min)'])
        #                 df['Hour'] = df['Date(min)'].dt.hour
        #                 output = df.groupby("Hour").sum().reset_index()
        #                 output["Hour"] = output["Hour"]
        #                 x = "Hour"
        #                 label = "Heure"
        #     else:
        #                 output = df.groupby("Jour").sum().reset_index()
        #                 output['Jour'] = pd.to_datetime(output['Jour'])
        #                 x = "Jour"
        #                 label = "Jour"
        #    # st.table(df)
        #     st.write(df)
        #     chart_anomalie_infraction(min_date1,max_date1,df,x,label)



















        col_0, col_1, col_time, col_4, col_5, col_6 = st.columns([3, 2, 3, 2, 2], gap="medium")

        # Within 'col_0' sub-column, handle date selection
        with col_0:
            # Check if 'min_date3' is present in session state, if not initialize it with the last date from the database
            if 'min_date3' not in st.session_state:
                st.session_state.min_date3 =data['new_date'].max()
                st.session_state.max_date3 = data['new_date'].max()

            # Retrieve the current values of min_date3 and max_date3 from session state
            min_date3 = st.session_state.min_date3
            max_date3 = st.session_state.max_date3

            # Create a date range selector and update min_date3 and max_date3 accordingly
            v = col_0.date_input("Sélecteur de date", (min_date3, max_date3), max_value=data['new_date'].max())
            if len(v) == 2:
                st.session_state.min_date3 = v[0]
                st.session_state.max_date3 = v[1]
            else:
                print("error")



        with col_1:
            start = "00:00"
            end = "23:59"
            times = []
            start = now = datetime.datetime.strptime(start, "%H:%M")
            end = datetime.datetime.strptime(end, "%H:%M")
            while now != end:
                times.append(str(now.strftime("%H:%M")))
                now += datetime.timedelta(minutes=1)
            times.append(end.strftime("%H:%M"))
            time_mul=st.multiselect('Departure hour:',times,max_selections=2)
            # Filter the available start time options based on min_date_infraction
            #option_date11 = Database.database_caller.filter_data1(infraction_df, min_date_infraction_)
        with col_4:
            selected_camera = st.selectbox("Camera", ["Select Camera",1, 2], index=0)

        with col_5:
            Filter = st.button("Filter")

    col_empty,tabs,col_empty=st.columns([0.01,1,0.01])
    with tabs:
        Anomaile,Infraction=st.tabs(["Anomaile","Infraction"])


             
        with Anomaile:              
                        intrusion_objet_df = data.loc[data['Description'].isin(['Intrusion', 'Objet sur le passage'])]
                        intrusion_objet_df = intrusion_objet_df[["ID_Vehicle", "ID_alertes","formatted_datetime", "date_", "Description", "chemin", "camera"]]
                        intrusion_objet_df['date_'] = pd.to_datetime(intrusion_objet_df['date_'])
                        intrusion_objet_df['Jour'] = intrusion_objet_df['date_'].dt.strftime('%Y-%m-%d')
                        intrusion_objet_df['Date(min)'] = intrusion_objet_df['date_'].dt.strftime('%H:%M')
                        intrusion_objet_df = intrusion_objet_df[["Jour", "Date(min)","formatted_datetime", "Description", "camera"]]
                        if Filter:
                                # Check if both start time and end time are selected
                                if time_end2 is None and time_start2 is None:
                                    st.error("Cette date n'est pas valide sélectionnez une date valide")
                                    return
                                else:
                                    # Filter the data based on the selected date range and time range
                                    intrusion_objet_df['formatted_datetime'] = pd.to_datetime(intrusion_objet_df['formatted_datetime'], format='%Y-%m-%d %H:%M')
                                    # Filter the DataFrame based on the selected camera
                                    intrusion_objet_df = intrusion_objet_df[
                                        (intrusion_objet_df["formatted_datetime"] >= merged_datetime_formatted_start) &
                                        (intrusion_objet_df["formatted_datetime"] <= merged_datetime_formatted_end)]
                                    intrusion_objet_df = intrusion_objet_df[intrusion_objet_df["camera"] == selected_camera]
                                    intrusion_objet_df = intrusion_objet_df[["Jour", "Date(min)", "Description", "camera"]]
                        else:
                            # Display the entire data
                            intrusion_objet_df = intrusion_objet_df[["Jour", "Date(min)", "Description", "camera"]]
                        anomalie_.anomalie(Anomaile,intrusion_objet_df,Filter,time_end2,time_start2,merged_datetime_formatted_start,merged_datetime_formatted_end,selected_camera)

        with Infraction:
                    infraction_df = data.loc[data['Description'] == 'Infraction véhicule']
                    infraction_df['date_'] = pd.to_datetime(infraction_df['date_'])
                    infraction_df['Jour'] = infraction_df['date_'].dt.strftime('%Y-%m-%d')
                    infraction_df['Date(min)'] = infraction_df['date_'].dt.strftime('%H:%M')
                    #infraction_df = infraction_df[["ID_Vehicle", "ID_alertes", "date_","formatted_datetime", "plaque_immatricule", "Description", "chemin", "camera"]]
                    #st.write(infraction)
                    if Filter:
                            # Check if both start time and end time are selected
                            if time_end2 is None and time_start2 is None:
                                st.error("Cette date n'est pas valide sélectionnez une date valide")
                                return
                            else:
                                # Filter the data based on the selected date range and time range
                                infraction_df['formatted_datetime'] = pd.to_datetime(infraction_df['formatted_datetime'], format='%Y-%m-%d %H:%M')
                                # Filter the DataFrame based on the selected camera
                                infraction_df = infraction_df[
                                    (infraction_df["formatted_datetime"] >= merged_datetime_formatted_start) &
                                    (infraction_df["formatted_datetime"] <= merged_datetime_formatted_end)]
                                infraction_df = infraction_df[infraction_df["camera"] == selected_camera]
                                infraction_df = infraction_df[["Jour", "Date(min)" ,"plaque_immatricule", "Description", "camera", "chemin"]]
                    else:
                        # Display the entire data
                            infraction_df = infraction_df[["Jour", "Date(min)","plaque_immatricule", "Description", "camera", "chemin"]]
                            infraction_df = infraction_df.rename(columns={"plaque_immatricule": "Plaque immatricule"})
                    infraction_.infraction(Infraction,infraction_df,Filter,time_end2,time_start2,merged_datetime_formatted_start,merged_datetime_formatted_end,selected_camera,col_6)
