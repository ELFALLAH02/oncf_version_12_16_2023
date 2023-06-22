import pandas as pd  # Importing the pandas library for data manipulation
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme, JsCode, AgGridReturn, ColumnsAutoSizeMode  # Importing necessary components from st_aggrid library
from st_aggrid.grid_options_builder import GridOptionsBuilder  # Importing GridOptionsBuilder for building grid options
import streamlit as st  # Importing Streamlit library for building web applications
import io  # Importing the io module for handling file input/output
import datetime  # Importing datetime module for working with dates and times
import streamlit.components.v1 as components  # Importing components from Streamlit for rendering HTML components
import plotly.express as px  # Importing Plotly Express for interactive plotting
import pandas as pd  # Importing the pandas library again
import Database.database_caller  # Importing custom module for database interactions
import plotly.graph_objs as go  # Importing graph objects from Plotly
import io  # Importing the io module again
import Database.Dataset  # Importing custom module for working with datasets
def Anomalie_():
    select = True  # Set the value of the variable 'select' to True

    if select:  # If the 'select' variable is True
        mydb, cursor = Database.Dataset.connect_to_database()  # Connect to the database and get the database object and cursor

        def check_database_state(mydb):
            if not mydb.is_connected():
                mydb.connect()  # Check the state of the database connection and connect if not connected

        def get_column_names(cursor):
            return [desc[0] for desc in cursor.description]  # Get the column names from the cursor

    def anomalie():
        check_database_state(mydb)  # Check the state of the database connection
        cursor = mydb.cursor()  # Get the database cursor
        query = "SELECT HOUR(alertes_filtrer.date_) AS hour, \
            MINUTE(alertes_filtrer.date_) AS minute, alertes_filtrer.id_v, alertes_filtrer.ID_alertes, alertes_filtrer.Description, alertes_filtrer.Checked, \
            alertes_filtrer.camera, alertes_filtrer.chemin, alertes_filtrer.date_, CONCAT(DATE_FORMAT(alertes_filtrer.date_, '%Y-%m-%d %H:%i')) AS formatted_datetime, \
            DATE(alertes_filtrer.date_) AS new_date FROM alertes_filtrer"  # SQL query to retrieve data from the database
        cursor.execute(query)  # Execute the SQL query
        column_names = get_column_names(cursor)  # Get column names from the cursor
        merged_df = [column_names] + cursor.fetchall()  # Fetch all rows from the cursor and add column names
        Merged_Vehicles_alertes = pd.DataFrame(merged_df[1:], columns=merged_df[0])  # Create a DataFrame from the fetched data
        Merged_Vehicles_alertes["Description"].replace({"stop": "Infraction véhicule"}, inplace=True)  # Replace "stop" with "Infraction véhicule" in the "Description" column
        return Merged_Vehicles_alertes  # Return the processed DataFrame

    data = anomalie()  # Call the 'anomalie' function to retrieve the data
    intrusion_objet_df = data.loc[data['Description'].isin(['intrusion'])]  # Filter the data based on the 'Description' column value
    intrusion_objet_df['date_'] = pd.to_datetime(intrusion_objet_df['date_'])  # Convert the 'date_' column to datetime format
    intrusion_objet_df['Jour'] = intrusion_objet_df['date_'].dt.strftime('%Y-%m-%d')  # Extract the date component from the 'date_' column
    intrusion_objet_df['Date(min)'] = intrusion_objet_df['date_'].dt.strftime('%H:%M')  # Extract the hour and minute component from the 'date_' column
    st.markdown('<style>' + open('./Style/anomalie.css').read() + '</style>', unsafe_allow_html=True)  # Apply custom CSS styles from a file

    # Define column layout using st.columns
    empty_col, col_display, empty_col1 = st.columns([0.01, 5, 0.01])

    with col_display:
        col_time_, col_0, col_1, col_4, col_5, col_6 = st.columns([2, 2, 2, 3, 2, 2], gap="medium")

        # Check if 'min_date_infraction' and 'max_date_infraction' are present in session state, if not initialize them with the current date
        if 'min_date_infraction' not in st.session_state and 'max_date_infraction' not in st.session_state:
            st.session_state.min_date_infraction = datetime.datetime.now().strftime('%Y-%m-%d')
            st.session_state.max_date_infraction = datetime.datetime.now().strftime('%Y-%m-%d')

        # Retrieve the current values of min_date_infraction and max_date_infraction from session state
        min_date_anomalie = st.session_state.min_date_infraction
        max_date_anomalie = st.session_state.max_date_infraction
 

        # Create a date range selector and update min_date_infraction and max_date_infraction accordingly
        min_date_anomalie_ = col_time_.date_input("Date de début")
        max_date_anomalie_ = col_0.date_input("Date de fin")
    with col_1:
        start = "00:00"
        end = "23:59"
        times = []
        start = now = datetime.datetime.strptime(start, "%H:%M")
        end = datetime.datetime.strptime(end, "%H:%M")
        
        # Create a list of time slots at 1-minute intervals from start to end time
        while now != end:
            times.append(str(now.strftime("%H:%M")))
            now += datetime.timedelta(minutes=1)
        
        times.append(end.strftime("%H:%M"))
        
        time_mul = st.multiselect('Temps:', times, max_selections=2)  # Allow users to select one or two time slots
        
        # Note: The selected time slots will be available in the 'time_mul' variable for further processing

    with col_4:
        selected_camera = st.selectbox("Caméra", ["Sélectionner une caméra", 1, 2], index=0)
        # Note: The selected camera option will be available in the 'selected_camera' variable for further processing

    with col_5:
        Filter = st.button("Filter")
        # Note: The 'Filter' button can be used to trigger further actions or filtering based on user inputs

       

    col_empty, tabs, col_empty = st.columns([0.01, 1, 0.01])

    with tabs:
        if Filter:
            if not time_mul and selected_camera == "Sélectionner une caméra":
                # Filter intrusion_objet_df based on min_date_anomalie_ and max_date_anomalie_
                intrusion_objet_df = intrusion_objet_df[(intrusion_objet_df["new_date"] >= min_date_anomalie_) & (intrusion_objet_df["new_date"] <= max_date_anomalie_)]
            elif not time_mul:
                # Filter intrusion_objet_df based on max_date_anomalie_ and selected_camera
                intrusion_objet_df = intrusion_objet_df[(intrusion_objet_df["new_date"] >= max_date_anomalie_) & (intrusion_objet_df["new_date"] <= max_date_anomalie_)]
                intrusion_objet_df = intrusion_objet_df[intrusion_objet_df["camera"] == selected_camera]
            elif time_mul:
                if time_mul[0] is not None:
                    # Convert time_mul[0] to datetime object and combine with min_date_anomalie_
                    time_obj1 = datetime.datetime.strptime(time_mul[0], "%H:%M").time()
                    full_datetime_1 = datetime.datetime.combine(min_date_anomalie_, time_obj1)

                if time_mul[1] is not None:
                    # Convert time_mul[1] to datetime object and combine with max_date_anomalie_
                    time_obj2 = datetime.datetime.strptime(time_mul[1], "%H:%M").time()
                    full_datetime_2 = datetime.datetime.combine(max_date_anomalie_, time_obj2)

                # Filter intrusion_objet_df based on full_datetime_1 and full_datetime_2
                intrusion_objet_df = intrusion_objet_df[(intrusion_objet_df["date_"] >= full_datetime_1) & (intrusion_objet_df["date_"] <= full_datetime_2)]

            intrusion_objet_df = intrusion_objet_df[["Jour", "Date(min)", "Description", "camera"]]
        else:
            intrusion_objet_df = intrusion_objet_df[["Jour", "Date(min)", "Description", "camera"]]

        # Configure grid options for displaying the DataFrame
        grid_options = GridOptionsBuilder().from_dataframe(intrusion_objet_df)
        grid_options.configure_selection('multiple', use_checkbox=True)
        grid_options.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
        grid_options.configure_auto_height(True)

        grid_options.configure_column(field="Date(min)", header_name="Date(min)", width=120)
        grid_options.configure_column(field="Jour", header_name="Jour", width=120)
        grid_options.configure_column(field="Description", header_name="Description", width=120)
        grid_options.configure_column(field="camera", header_name="camera", width=100)

        gridoptions = grid_options.build()

        anomalie_table = AgGrid(
                        intrusion_objet_df,
                        gridOptions=gridoptions,
                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                        fit_columns_on_grid_load=True,
                        height=500,
                        width="100%",
                        #allow_unsafe_jscode=True,
                        theme=AgGridTheme.MATERIAL,
                        # Add the custom cell renderer to the "chemin" column
                    )


        if anomalie_table["selected_rows"]:
            selected_rows=anomalie_table['selected_rows']
            # Convert the selected rows to a DataFrame
            selected_df = pd.DataFrame(selected_rows)
            column_3_selected_df = selected_df['Jour']
            column_4_selected_df = selected_df['Date(min)']

            # Check if the values in columns 3 and 4 of `other_df` exist in `selected_df`
            mask = intrusion_objet_df['Jour'].isin(column_3_selected_df) & intrusion_objet_df["Date(min)"].isin(column_4_selected_df)
            intrusion_objet_df=intrusion_objet_df[mask]
            # Create a new table with rows from `other_df` where the values match `selected_df`

        def download_excel(df):
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            workbook = writer.book
            worksheet = workbook.add_worksheet("Anomalie")

            # Set column widths
            column_widths = {
                'A': 0,  # Example: Set column A width to 12
                'B': 20,  # Example: Set column B width to 10
                'C': 20,  # Example: Set column C width to 10
                'D': 25,  # Example: Set column C width to 25
                'E': 25,  # Example: Set column C width to 25
            }
            # Set text alignment for columns D to I
            centered_columns = ['A', 'B', 'C', 'D', 'E']
            cell_format = workbook.add_format({'align': 'center'})
            for col in centered_columns:
                worksheet.set_column(f'{col}:{col}', None, cell_format)

            # Apply column widths
            for col, width in column_widths.items():
                worksheet.set_column(f'{col}:{col}', width)

            row_heights = {
                0: 20,
                # Example: Set height of row 1 to 20
            }
            for row, height in row_heights.items():
                worksheet.set_row(row, height)
            df["Jour"] = df["Jour"].values.astype('str')
            df.to_excel(writer, sheet_name='Anomalie', index=True)
            writer.save()
            output.seek(0)
            return output

        if intrusion_objet_df.empty:
            st.warning("Pas de données disponibles")
        else:
            # Generate and download the Excel file when the "Export" button is clicked
            excel_file = download_excel(intrusion_objet_df)
            current_datetime = datetime.datetime.now()
            # Format the date and time in the desired format
            formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H:%M:%S")
            file_name = f'Anomalie_{formatted_datetime}.xlsx'
            col_6.download_button(label='Export', data=excel_file, file_name=file_name, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
