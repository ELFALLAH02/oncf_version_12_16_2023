import pandas as pd  # Import pandas library as pd for data manipulation and analysis
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme, JsCode, AgGridReturn, ColumnsAutoSizeMode  # Import necessary components from the st_aggrid library for displaying AgGrid tables
from st_aggrid.grid_options_builder import GridOptionsBuilder  # Import GridOptionsBuilder for building the options for AgGrid
from functions.video_button import BtnCellRenderer_Chemin  # Import BtnCellRenderer_Chemin from the functions.video_button module
import streamlit as st  # Import streamlit library as st for building the web application
import io  # Import io module for handling file input/output operations
import datetime  # Import datetime module for working with dates and times
import streamlit.components.v1 as components  # Import components from streamlit for adding components to the app
import plotly.express as px  # Import plotly express library for creating interactive plots
import pandas as pd  # Import pandas library as pd for data manipulation and analysis
import Database.database_caller  # Import a module called database_caller from the Database package
import plotly.graph_objs as go  # Import graph_objs from plotly for creating graph objects
import io  # Import io module for handling file input/output operations
import Database.Dataset
def Infraction():
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
    data =Merged_Vehicles_alertes()  # Accessing the 'anomalie' attribute from the 'database_caller' object in the 'Database' module
    infraction_df = data.loc[data['Description'] == 'Infraction véhicule']
    # Convert 'date_' column to datetime format
    infraction_df['date_'] = pd.to_datetime(infraction_df['date_'])

    # Extract 'Jour' and 'Date(min)' from the 'date_' column
    infraction_df['Jour'] = infraction_df['date_'].dt.strftime('%Y-%m-%d')
    infraction_df['Date(min)'] = infraction_df['date_'].dt.strftime('%H:%M')    
    st.markdown('<style>' + open('./Style/anomalie.css').read() + '</style>', unsafe_allow_html=True)  # Applying custom CSS styles from the 'anomalie.css' file
    empty_col, col_display, empty_col1 = st.columns([0.01, 5, 0.01])  # Creating columns for layout purposes using Streamlit's 'columns' function
    with col_display:
        col_time_1, col_time_2, col_1, col_4, col_5, col_6 = st.columns([2, 2, 2, 3, 2, 2], gap="medium")
        # Creating multiple sub-columns within the 'col_display' column for different purposes
        # Check if 'min_date_infraction' is present in session state, if not initialize it with the last date from the database
        if 'min_date_infraction' not in st.session_state and 'max_date_infraction' not in st.session_state:
            st.session_state.min_date3 = datetime.datetime.now().strftime('%Y-%m-%d')
            st.session_state.max_date3 = datetime.datetime.now().strftime('%Y-%m-%d')
        # Retrieve the current values of min_date3 and max_date3 from session state
        min_date3_contage = st.session_state.min_date3
        max_date3_contage = st.session_state.max_date3

        # Create a date range selector and update min_date3 and max_date3 accordingly
        min_date_infraction_ = col_time_1.date_input("Date de début ", value=min_date3_contage)
        max_date_infraction_ = col_time_2.date_input("Date de fin ", value=max_date3_contage)
        # Within 'col_1' sub-column, handle start time selection
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
            time_mul=st.multiselect('Temps:',times,max_selections=2)
            # Filter the available start time options based on min_date_infraction
            #option_date11 = Database.database_caller.filter_data1(infraction_df, min_date_infraction_)
        with col_4:
            selected_camera = st.selectbox("Caméra", ["Sélectionner une caméra",1, 2], index=0)

        with col_5:
            Filter = st.button("Filter")

    # Create columns for layout
    col_empty, tabs, col_empty = st.columns([0.01, 1, 0.01])

    # Filter the data to include only 'Infraction véhicule' records


    with tabs:
        # Check if the 'Filter' button is clicked
        if Filter:
            if not time_mul and selected_camera=="Sélectionner une caméra":
              infraction_df = infraction_df[(infraction_df["new_date"] >=min_date_infraction_ ) & (infraction_df["new_date"] <= max_date_infraction_)]   
            elif not time_mul:
                infraction_df = infraction_df[(infraction_df["new_date"] >=min_date_infraction_ ) & (infraction_df["new_date"] <= max_date_infraction_)]   
                infraction_df = infraction_df[infraction_df["camera"] == selected_camera]
            elif time_mul:      
                if time_mul[0] is not None:
                            time_obj1 = datetime.datetime.strptime(time_mul[0], "%H:%M").time()  # Convert string to `datetime.time` object
                            full_datetime_1 = datetime.datetime.combine(min_date_infraction, time_obj1)

                if time_mul[1] is not None:
                            time_obj2 = datetime.datetime.strptime(time_mul[1], "%H:%M").time()  # Convert string to `datetime.time` object
                            full_datetime_2 = datetime.datetime.combine(max_date_infraction, time_obj2)
                infraction_df = infraction_df[(infraction_df["date_"] >=full_datetime_1 ) & (infraction_df["date_"] <= full_datetime_2)]   
            infraction_df = infraction_df[["Jour", "Date(min)", "plaque_immatricule", "Description", "camera", "chemin"]]
            infraction_df = infraction_df.rename(columns={"plaque_immatricule": "Plaque immatricule"})


        else:
            # Display the entire data if the 'Filter' button is not clicked
            infraction_df = infraction_df[["Jour", "Date(min)", "plaque_immatricule", "Description", "camera", "chemin"]]
            infraction_df = infraction_df.rename(columns={"plaque_immatricule": "Plaque immatricule"})

        # Configure the grid options for displaying the data
        grid_options = GridOptionsBuilder().from_dataframe(infraction_df)

        # Enable multiple selection using checkboxes in the grid
        grid_options.configure_selection('multiple', use_checkbox=True)

        # Configure pagination options for the grid
        grid_options.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)

        # Automatically adjust the height of the grid based on the data
        grid_options.configure_auto_height(True)

        # Configure the columns in the grid
        grid_options.configure_column(field="chemin", header_name="chemin", hide=True)
        grid_options.configure_column(field="camera", header_name="camera", width=120)
        grid_options.configure_column(field="Description", header_name="Description", width=160)
        grid_options.configure_column(field="Date(min)", header_name="Date(min)", width=160)
        grid_options.configure_column(field="Jour", header_name="Jour", width=160)
        grid_options.configure_column(field="Plaque immatricule", header_name="Plaque immatricule", width=200)

        # Build the grid options
        gridoptions = grid_options.build()


        gridoptions['columnDefs'].append({
            "field": "Preuve",
            "header": "Action",
            "cellRenderer": BtnCellRenderer_Chemin,  # Custom cell renderer for the 'Valide' button
            "cellRendererParams": {
                "border": "none",
                "background": "rgb(15, 133, 250)",
                "height": "50px",
                "width": "160px",
                "color": "#FFFFFF",
            },
        })

        # Create an AgGrid component with the provided data and grid options
        infraction_table = AgGrid(
            infraction_df,
            gridOptions=gridoptions,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            height=500,
            width="100%",
            allow_unsafe_jscode=True,
            theme=AgGridTheme.MATERIAL,
            # Add the custom cell renderer to the "chemin" column
        )

        # Remove the "chemin" column from the DataFrame
        infraction_df = infraction_df.drop("chemin", axis=1)
        infraction_df = infraction_df[["Jour", "Date(min)", "Plaque immatricule", "Description", "camera"]]

        if infraction_table["selected_rows"]:
            selected_rows = infraction_table['selected_rows']
            # Convert the selected rows to a DataFrame
            selected_df = pd.DataFrame(selected_rows)
            column_3_selected_df = selected_df['Plaque immatricule']
            # Check if the values in columns 3 and 4 of `other_df` exist in `selected_df`
            mask = infraction_df['Plaque immatricule'].isin(column_3_selected_df)
            infraction_df = infraction_df[mask]
            # Create a new table with rows from `other_df` where the values match `selected_df`

        def download_excel(df):
            # Function to generate and download an Excel file from a DataFrame
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

            # Generate and download the Excel file when the "Export" button is clicked
        excel_file = download_excel(infraction_df)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H:%M:%S")
        file_name = f'infraction_{formatted_datetime}.xlsx'
        col_6.download_button(label='Export', data=excel_file, file_name=file_name, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

