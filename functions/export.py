import pandas as pd
import numpy as np
def export_table(df_table_base):
    # Convert columns to the desired datetime format
    df_table_base['Heure_passage'] = pd.to_datetime(df_table_base['Heure_passage'])  # Convert 'Heure_passage' column to datetime format
    df_table_base['Jour'] = df_table_base['Heure_passage'].dt.date  # Extract the date from 'Heure_passage' and store it in the 'Jour' column
    df_table_base['Date(min)'] = df_table_base['Heure_passage'].dt.strftime('%H:%M')  # Extract the time in the format HH:MM from 'Heure_passage' and store it in the 'Date(min)' column
    df_table_base['formatted_datetime'] = pd.to_datetime(df_table_base['formatted_datetime'], format='%Y-%m-%d %H:%M')  # Convert 'formatted_datetime' column to datetime format with a specific format
    
    selected_columns = ['Heure_passage', 'Date(min)', 'Jour', 'ID_Vehicle', 'classe', 'sens', "formatted_datetime"]  # List of columns to select from the DataFrame
    df_selected = df_table_base[selected_columns]  # Select the desired columns from the DataFrame
    
    df_grouped = df_selected.groupby(['Jour', 'Date(min)', 'sens', 'classe', "formatted_datetime"])['ID_Vehicle'].nunique().reset_index(name='Number of Vehicles')  # Group the selected data by multiple columns and calculate the number of unique vehicles for each group
    df_grouped = df_grouped.fillna(0)  # Fill any missing values in the DataFrame with zeros
    
    all_sens = set(df_grouped['sens'].unique())  # Get the unique values of 'sens' column
    if len(all_sens) <= 1:  # Check if both sens values (0 and 1) are present in df_grouped
        missing_sens = set([0, 1]) - all_sens  # Calculate the missing sens value(s)
        missing_sens_data = []
        for sens in missing_sens:
            missing_sens_data.extend([{
                'Jour': Jour,
                'Date(min)': date_min,
                'sens': sens,
                'classe': classe,
                'Number of Vehicles': 0
            } for Jour in df_grouped['Jour'].unique()
            for date_min in df_grouped[df_grouped['Jour'] == Jour]['Date(min)'].unique()
            for classe in df_grouped[df_grouped['Jour'] == Jour]['classe'].unique()])

        missing_sens_df = pd.DataFrame(missing_sens_data)  # Create a DataFrame with missing "sens" values
        df_grouped = pd.concat([df_grouped, missing_sens_df], ignore_index=True)  # Append the missing sens DataFrame to df_grouped
        
    df_grouped = df_grouped.sort_values(by=['Jour', 'Date(min)', 'sens'])  # Sort the DataFrame by 'Jour', 'Date(min)', and 'sens' columns
    df_grouped = df_grouped.reset_index(drop=True)  # Reset the index of the DataFrame

    table_1 = df_grouped[df_grouped['sens'] == 1].drop(['sens'], axis=1)  # Select rows where 'sens' is 1 and remove the 'sens' column
    table_2 = df_grouped[df_grouped['sens'] == 0].drop(['sens'], axis=1)  # Select rows where 'sens' is 0 and remove the 'sens' column

    all_classes = {'C1', 'C2', 'C3'}  # Set of all classes
    
    missing_classes_table_1 = [{'Jour': Jour, 'Date(min)': date_min, 'classe': classe, 'Number of Vehicles': 0}
                               for Jour, date_min in zip(table_1['Jour'].unique(), table_1['Date(min)'].unique())
                               for classe in all_classes if classe not in table_1[table_1['Jour'] == Jour]['classe'].unique()]  # Create a list of dictionaries for missing classes in table_1
    
    missing_classes_table_2 = [{'Jour': Jour, 'Date(min)': date_min, 'classe': classe, 'Number of Vehicles': 0}
                               for Jour, date_min in zip(table_2['Jour'].unique(), table_2['Date(min)'].unique())
                               for classe in all_classes if classe not in table_2[table_2['Jour'] == Jour]['classe'].unique()]  # Create a list of dictionaries for missing classes in table_2
    
    table_1 = pd.concat([table_1, pd.DataFrame(missing_classes_table_1)], ignore_index=True)  # Append the missing classes to table_1
    table_2 = pd.concat([table_2, pd.DataFrame(missing_classes_table_2)], ignore_index=True)  # Append the missing classes to table_2
    
    table_1 = table_1.groupby(['Jour', 'Date(min)', 'classe']).sum().unstack(fill_value=0)  # Group table_1 by 'Jour' and 'Date(min)' columns, sum the values for each class, and unstack the table
    table_2 = table_2.groupby(['Jour', 'Date(min)', 'classe']).sum().unstack(fill_value=0)  # Group table_2 by 'Jour' and 'Date(min)' columns, sum the values for each class, and unstack the table
    
    merged_table = pd.concat([table_1, table_2], axis=1, keys=['Comptage manuelle de véhicules par sens positif (Camera 2 -> Camera 1)', 'Comptage manuelle de véhicules par sens négatif (Camera 1 -> Camera 2)'])  # Concatenate table_1 and table_2 horizontally with column keys
    
    merged_table.columns = pd.MultiIndex.from_product([merged_table.columns.levels[0], ['C1', 'C2', 'C3']])  # Create a MultiIndex for the column names
    
    merged_table = merged_table.fillna(0).replace(np.inf, 0)  # Fill any missing or infinite values with zeros
    
    merged_table = merged_table.astype(int)  # Convert the values in the merged table to integers
    
    merged_table = merged_table.reset_index()  # Reset the index of the merged table
    
    column_mapping = {
        'C1': 'Classe 1',
        'C2': 'Classe 2',
        'C3': 'Classe 3'
    }  # Dictionary for mapping column names
    
    merged_table = merged_table.rename(columns=column_mapping)  # Rename the columns of the merged table using the dictionary
    
    return merged_table  # Return the merged table
