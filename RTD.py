import streamlit as st  # Importing the Streamlit library for creating web apps
import datetime  # Importing the datetime module for working with dates and times
import streamlit.components.v1 as components  # Importing Streamlit components for rendering HTML
import plotly.express as px  # Importing Plotly Express for interactive visualizations
import pandas as pd  # Importing Pandas for data manipulation and analysis
from st_aggrid import (
    AgGrid,
    GridUpdateMode,
    AgGridTheme,
    JsCode,
    AgGridReturn,
    ColumnsAutoSizeMode,
)  # Importing st_aggrid for displaying data grids in Streamlit
from st_aggrid.grid_options_builder import GridOptionsBuilder  # Importing grid options builder for AgGrid
import numpy as np  # Importing NumPy for numerical computing
import Database.database_caller  # Importing database_caller module from Database package
import matplotlib.pyplot as plt  # Importing Matplotlib for data visualization
import plotly.graph_objs as go  # Importing Plotly graph objects for creating plots
import functions.data_checker  # Importing data_checker module from functions package
import io  # Importing io module for working with input/output
import functions.table_format  # Importing table_format module from functions package
import functions.Charts  # Importing Charts module from functions package
import functions.export  # Importing export module from functions package
import mysql.connector  # Importing the MySQL Connector for connecting to MySQL database
import Database.Dataset  # Importing Dataset module from Database package

def rtd():
    """
    Real-Time Data (RTD) function for processing and retrieving data from a database.
    """
    select_rdt = True
    
    if select_rdt:
        mydb, cursor = Database.Dataset.connect_to_database()  # Connect to the database
        
        def check_database_state(mydb):
            """
            Check the state of the database and connect if not connected.
            """
            if not mydb.is_connected():
                mydb.connect()
        
        def get_column_names(cursor):
            """
            Retrieve column names from the database cursor.
            """
            return [desc[0] for desc in cursor.description]
    
    def contage_select():
        """
        Query the database and process the retrieved data.
        """
        check_database_state(mydb)  # Check the state of the database
        cursor = mydb.cursor()  # Create a cursor object
        
        query = """
            SELECT historique_passage_filtrer.*,
                HOUR(historique_passage_filtrer.Heure_passage) AS hour,
                DAY(historique_passage_filtrer.Heure_passage) AS day,
                MONTH(historique_passage_filtrer.Heure_passage) AS month,
                MINUTE(historique_passage_filtrer.Heure_passage) AS minute,
                CONCAT(DATE(historique_passage_filtrer.Heure_passage), ' ',
                    LPAD(HOUR(historique_passage_filtrer.Heure_passage), 2, '0'), ':',
                    LPAD(MINUTE(historique_passage_filtrer.Heure_passage), 2, '0')) AS formatted_datetime,
                DATE(historique_passage_filtrer.Heure_passage) AS new_date
            FROM historique_passage_filtrer
        """
        cursor.execute(query)  # Execute the query
        
        column_names = get_column_names(cursor)  # Get column names from the cursor
        
        merged_data = [column_names] + cursor.fetchall()  # Fetch all rows and add column names
        
        # Create a DataFrame from the retrieved data
        Merged_Vehicles_Historique_passage = pd.DataFrame(merged_data[1:], columns=merged_data[0])
        
        # Replace values in the "class" column
        Merged_Vehicles_Historique_passage["class"].replace(
            {"SEDAN": "C2", "TRUCK": "C3", "VEHICLE_UNCLASSED": "C1"},
            inplace=True
        )
        
        # Rename the "class" column to "classe"
        Merged_Vehicles_Historique_passage.rename(columns={"class": "classe"}, inplace=True)
        
        return Merged_Vehicles_Historique_passage

# The code above defines the necessary imports and the functions for real-time data retrieval and processing.
# However, it does not include the code for utilizing these functions or any other logic.
# Additional code is required to utilize these functions and build the desired application.
# The provided code snippet mainly focuses on importing required modules and defining the functions.

    data = contage_select()  # Call the contage_select function to retrieve the data

    # Add custom CSS to the Streamlit application
    st.markdown('<style>' + open('./Style/RTD.css').read() + '</style>', unsafe_allow_html=True)

    # Create columns for layout
    empty_col, col_display, empty_col1 = st.columns([0.01, 5, 0.01])

    # Within the 'col_display' column, create sub-columns for date inputs
    with col_display:
        col_min_date, col_max_date, col_advance_filter = st.columns([2, 2, 0.01])

        # Check if 'min_date1' and 'max_date1' session states are already set
        if 'min_date1' not in st.session_state and "max_date1" not in st.session_state:
            # Set default values for 'min_date1' and 'max_date1' using current date
            st.session_state.min_date1 = datetime.datetime.now().strftime('%Y-%m-%d')
            st.session_state.max_date1 = datetime.datetime.now().strftime('%Y-%m-%d')

        # Retrieve the current values of min_date1 and max_date1 from session state
        min_date_contage = st.session_state.min_date1
        max_date_contage = st.session_state.max_date1
        min_date_1 = datetime.datetime.strptime(min_date_contage, "%Y-%m-%d").date()
        max_date_2 = datetime.datetime.strptime(max_date_contage, "%Y-%m-%d").date()

        # Create a date range selector and update min_date1 and max_date1 accordingly
        min_date1 = col_min_date.date_input("Date de début", value=min_date_1)
        max_date1 = col_max_date.date_input("Date de fin", value=max_date_2)


    # Create columns for layout
    col_space_chart_left, col_chart_1, col_space_chart_2_right = st.columns([0.01, 1, 0.01])

    # Within the 'col_chart_1' column, perform the following actions
    with col_chart_1:
        # Filter the data based on the selected date range
        df = data[(data["new_date"] >= min_date1) & (data["new_date"] <= max_date1)]

        # Check if the filtered DataFrame is empty
        if not df.empty:
            # Format the DataFrame using the 'tabel' function
            df = functions.table_format.tabel(df)

            # Select the desired columns from the DataFrame
            df = df[["Jour", "Date(min)", "Total Vehicules", "Total Classe 1", "Total Classe 2", "Total Classe 3", "Sens 1", "Sens 0"]]
            
            # Perform additional data manipulation or add mock data if needed
            # ...

            # Determine the x-axis variable and its corresponding label based on the selected date range
            if max_date1 == min_date1:
                df['Date(min)'] = pd.to_datetime(df['Date(min)'])
                df['Hour'] = df['Date(min)'].dt.hour
                output = df.groupby("Hour").sum().reset_index()
                output["Hour"] = output["Hour"]
                x = "Hour"
                label = "Heure"
            else:
                output = df.groupby("Jour").sum().reset_index()
                output['Jour'] = pd.to_datetime(output['Jour'])
                x = "Jour"
                label = "Jour"

        # Create tabs for selecting between 'sens' and 'Classe' charts
       

        # Check if the DataFrame is not empty
        sens_tab, classe_tab = st.tabs(["Sens", "Classe"])

                # Check if the DataFrame is not empty
                    # Display the 'chart_par_sens' function within the 'sens' tab
        with sens_tab:
                    if df.empty:
                        empty_fig = px.line(title='Pas de données disponibles')
                        empty_fig.update_layout(width=1100, height=400, title='Pas de données disponibles')
                        st.write(empty_fig)
                    else:
                      functions.Charts.chart_par_sens(output, x, label,max_date1,min_date1)
                    
                    # Display the 'chart_par_classe' function within the 'Classe' tab
        with classe_tab:
                    if df.empty:
                        empty_fig = px.line(title='Pas de données disponibles')
                        empty_fig.update_layout(width=1100, height=400, title='Pas de données disponibles')
                        st.write(empty_fig)
                    else:
                        functions.Charts.chart_par_classe(output, x, label,max_date1,min_date1)
                #else:
    # Create columns for layout
    col_space_1, col, col_space_2 = st.columns([0.01, 5, 0.01])

    # Within the 'col' column, perform the following actions

    with col:
        # Create sub-columns for layout
        col_start_time1, col_start_time2, col_1, col_5, col_6 = st.columns([2, 2, 2, 2, 2], gap="medium")

        if 'min_date3' not in st.session_state and 'max_date3' not in st.session_state:
            st.session_state.min_date3 = datetime.datetime.now().strftime('%Y-%m-%d')
            st.session_state.max_date3 = datetime.datetime.now().strftime('%Y-%m-%d')

        # Create a date range selector and update min_date3 and max_date3 accordingly
        min_date_ = col_start_time1.date_input("Date de début ")
        max_date_ = col_start_time2.date_input("Date de fin ")

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
            time_mul = st.multiselect('Temps', times, max_selections=2)

        with col_5:
            filter = st.button("Filter")

    # Create columns for table layout
    col_space_table, col_table, col_space_table_ = st.columns([0.01, 1, 0.01])

    # Within 'col_table' column, perform the following actions
    with col_table:
        df_table = pd.DataFrame()
        # Check if the filter button is clicked
        if filter:
            df_table_base = data
            if not time_mul:
                df_grouped = data[(data["new_date"] >= min_date_) & (data["new_date"] <= max_date_)]
                df_table = functions.table_format.tabel(df_table_base)
                df_table['Jour'] = pd.to_datetime(df_table['Jour']).dt.date
                df_table = df_table[(df_table["Jour"] >= min_date_) & (df_table["Jour"] <= max_date_)]
                df_table = df_table[["Jour", "Date(min)", "Total Vehicules", "Total Classe 1", "Total Classe 2",
                                    "Total Classe 3", "Sens 1", "Sens 0"]]
            else:
                if time_mul:
                    if time_mul[0] is not None:
                        time_obj1 = datetime.datetime.strptime(time_mul[0], "%H:%M").time()
                        full_datetime_1 = datetime.datetime.combine(min_date_, time_obj1)
                    if time_mul[1] is not None:
                        time_obj2 = datetime.datetime.strptime(time_mul[1], "%H:%M").time()
                        full_datetime_2 = datetime.datetime.combine(max_date_, time_obj2)
                        df_grouped = data[(data["Heure_passage"] >= full_datetime_1) &
                                        (data["Heure_passage"] <= full_datetime_2)]
                        df_table = functions.table_format.tabel(df_table_base)
                        df_table = df_table[(df_table["Heure_passage"] >= full_datetime_1) &
                                            (df_table["Heure_passage"] <= full_datetime_2)]
                        df_table = df_table[["Jour", "Date(min)", "Total Vehicules", "Total Classe 1", "Total Classe 2",
                                            "Total Classe 3", "Sens 1", "Sens 0"]]
        else:
            # Display the entire data
            df_grouped = data
            df_table_base = data
            df_table = functions.table_format.tabel(df_table_base)
            df_table = df_table[["Jour", "Date(min)", "Total Vehicules", "Total Classe 1", "Total Classe 2",
                                "Total Classe 3", "Sens 1", "Sens 0"]]

        # Configure grid options for the DataFrame table
        grid_options = GridOptionsBuilder().from_dataframe(df_table)
        grid_options.configure_selection('multiple', use_checkbox=True)  # Adding checkbox for multiple selection
        grid_options.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
        grid_options.configure_auto_height(True)
        grid_options.configure_column(field="Jour", header_name="Jour", width=130)
        grid_options.configure_column(field="Date(min)", header_name="Date(min)", width=90)
        grid_options.configure_column(field="Total Vehicules", header_name="Total Vehicules", width=120)
        grid_options.configure_column(field="Total Classe 1", header_name="Total Classe 1", width=110)
        grid_options.configure_column(field="Total Classe 2", header_name="Total Classe 2", width=110)
        grid_options.configure_column(field="Total Classe 3", header_name="Total Classe 3", width=110)
        grid_options.configure_column(field="Sens 1", header_name="Sens 1", width=90)
        grid_options.configure_column(field="Sens 0", header_name="Sens 0", width=90)

        # Render the AgGrid component
        ag_grid = AgGrid(
            df_table,
            gridOptions=grid_options.build(),
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            height=500,
            width="100%",
            theme=AgGridTheme.MATERIAL
        )

        # Get the selected rows from the AgGrid component
        if ag_grid["selected_rows"]:
            selected_rows = ag_grid['selected_rows']
            # Convert the selected rows to a DataFrame
            selected_df = pd.DataFrame(selected_rows)
            column_3_selected_df = selected_df['Jour']
            column_4_selected_df = selected_df['Date(min)']

            # Check if the values in columns 3 and 4 of `other_df` exist in `selected_df`
            mask = df_grouped['Jour'].isin(column_3_selected_df) & df_grouped['Date(min)'].isin(column_4_selected_df)

            # Create a new table with rows from `other_df` where the values match `selected_df`
            df_grouped = df_table_base[mask]

        def download_excel(df):
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            workbook = writer.book
            worksheet = workbook.add_worksheet("Comptage")

            # Set column widths
            column_widths = {
                'A': 0,  # Example: Set column A width to 12
                'B': 10,  # Example: Set column B width to 10
                'C': 10,  # Example: Set column C width to 15
                'D': 25,  # Example: Set column C width to 15
                'E': 25,  # Example: Set column C width to 15
                'F': 25,  # Example: Set column C width to 15
                'G': 25,  # Example: Set column C width to 15
                'H': 25,  # Example: Set column C width to 15
                'I': 25  # Example: Set column C width to 15
            }
            # Set text alignment for columns D to I
            centered_columns = ['D', 'E', 'F', 'G', 'H', 'I']
            cell_format = workbook.add_format({'align': 'center'})
            for col in centered_columns:
                worksheet.set_column(f'{col}:{col}', None, cell_format)

            # Apply column widths
            for col, width in column_widths.items():
                worksheet.set_column(f'{col}:{col}', width)

            row_heights = {
                0: 25,
                1: 20,
                2: 0,
            }
            for row, height in row_heights.items():
                worksheet.set_row(row, height)

            df["Jour"] = df["Jour"].values.astype('str')
            df.to_excel(writer, sheet_name='Comptage', index=True)
            writer.save()
            output.seek(0)
            return output

        if df_grouped.empty:
            st.warning("Pas de données disponibles")
        else:
            excel_file = download_excel(functions.export.export_table(df_grouped))
            current_datetime = datetime.datetime.now()
            # Format the date and time in the desired format
            formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H:%M:%S")

            # Add the formatted date and time to the file name
            file_name = f"Comptage_{formatted_datetime}.xlsx"
            col_6.download_button(label='Export', data=excel_file, file_name=file_name,
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Use the modified file name in the download_button function
