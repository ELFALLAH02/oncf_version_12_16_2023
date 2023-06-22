import streamlit as st  # Import the Streamlit library for building web apps
import pandas as pd  # Import the pandas library for data manipulation

# Define a function to transform the input DataFrame
def tabel(df_table):
    
    # Convert 'Heure_passage' column to datetime format
    df_table['Heure_passage'] = pd.to_datetime(df_table['Heure_passage'])
    
    # Extract date component and assign it to 'Jour' column
    df_table['Jour'] = df_table['Heure_passage'].dt.strftime('%Y-%m-%d')
    
    # Extract time component and assign it to 'Date(min)' column
    df_table['Date(min)'] = df_table['Heure_passage'].dt.strftime('%H:%M')
    
    # Group the DataFrame by 'Jour' and 'Date(min)' columns
    grouped = df_table.groupby(['Jour', 'Date(min)'])
    
    # Calculate the count of occurrences for each combination of 'classe' and 'sens'
    totals = grouped['classe'].value_counts().unstack(fill_value=0)
    
    # Rename the columns of 'totals' DataFrame
    totals.columns = ["Total Classe "+str(i) for i in range(1, len(totals.columns)+1)]
    
    # Calculate the count of occurrences for each 'sens' in each group
    sens_totals = grouped['sens'].apply(lambda x: x.value_counts().reindex([0, 1]).fillna(0).astype(int)).unstack(fill_value=0)

    # Rename the columns of 'sens_totals' DataFrame
    sens_totals.columns = ["Sens "+str(i) for i in range(0, len(sens_totals.columns))]

    # Concatenate 'totals' and 'sens_totals' horizontally
    output = pd.concat([totals, sens_totals], axis=1).reset_index().sort_values(['Jour', 'Date(min)'])
    
    if "Total Classe 1" not in output.columns:
        output["Total Classe 1"] = 0
    if "Total Classe 2" not in output.columns:
        output["Total Classe 2"] = 0
    if "Total Classe 3" not in output.columns:
        output["Total Classe 3"] = 0
    if "Sens 0" not in output.columns:
        output["Sens 0"] = 0
    if "Sens 1" not in output.columns:
        output["Sens 1"] = 0
    
    # Add 'formatted_datetime' column to the DataFrame
    output["Heure_passage"] = grouped['Heure_passage'].first().values
    # Calculate the total number of vehicles for each group
    output["Total Vehicules"] = output["Total Classe 1"] + output["Total Classe 2"] + output["Total Classe 3"]
    
    # Select and reorder the columns of the DataFrame
    output = output[["Jour", "Date(min)", "Heure_passage", "Total Vehicules", "Total Classe 1", "Total Classe 2", "Total Classe 3", "Sens 0", "Sens 1"]]
    
    # Return the modified DataFrame as output
    return output
