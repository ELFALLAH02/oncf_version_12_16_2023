import streamlit as st  # Importing the Streamlit library for creating web apps
import plotly.express as px  # Importing the Plotly Express library for interactive plots
import Database.database_caller  # Importing the database caller module
import functions.data_checker  # Importing the data checker module

  # Caching data to improve performance

# Define a function named 'chart_anomalie_infraction' that takes five parameters: 'min_date1', 'max_date1', 'df', 'x', and 'label'
def chart_anomalie_infraction(min_date1, max_date1, df, x, label):
    if min_date1 <= max_date1:
        if functions.data_checker.checker(min_date1, max_date1, Database.database_caller.data) is True:
            if x == "Hour":
                label_date = "à l'heure:"
            else:
                label_date = "le jour"
            
            # Create a line plot using Plotly Express
            fig = px.line(df, x=x,
                          #color_discrete_map={'Total Classe 1': '#003f5c', 'Total Classe 2': '#ff6361', 'Total Classe 3': '#ffa600'},
                          title='Nombre de véhicules par classe')
            
            fig.update_layout(width=1100, height=400)
            
            # Add scatter plots for each class with hover information
            fig.add_scatter(x=df[x], y=df['Intrusion'], mode='lines+markers', name='Classe 1',
                            hovertemplate="Total Classe 1<br>" + label_date + ":%{x}<br>" "Nombre des véhicules: %{y}<br>",
                            line={'color': '#003f5c'})

            fig.add_scatter(x=df[x], y=df['Objet sur le passage'], mode='lines+markers', name='Classe 2',
                            hovertemplate="Total Classe 2<br>" + label_date + ":%{x}<br>" "Nombre des véhicules: %{y}<br>",
                            line={'color': '#ff6361'})

            fig.add_scatter(x=df[x], y=df['Infraction véhicule'], mode='lines+markers', name='Classe 3',
                            hovertemplate="Total Classe 3<br>" + label_date + ":%{x}<br>" "Nombre des véhicules: %{y}<br>",
                            line={'color': '#ffa600'})
            # Set x-axis label and formatting
            fig.update_xaxes(title_text=label)
            
            if x == "Hour":
                fig.update_xaxes(range=['00', '23'], dtick='01')
            
            fig.update_yaxes(title_text='Total Vehicules', tickformat=',.0f')
            
            # Display the plot using Streamlit
            st.write(fig)
        elif functions.data_checker.valid_x == 'end_checker_inv':
            st.warning('The End-Date does not exist', icon="⚠️")  # Display a warning message if the end date is invalid
        elif functions.data_checker.valid_x == 'start_checker_inv':
            st.warning('The Start-Date does not exist', icon="⚠️")  # Display a warning message if the start date is invalid
        elif functions.data_checker.valid_x == 'both invalid':
            st.warning('Both dates do not exist', icon="⚠️")  # Display a warning message if both dates are invalid
    else:
        st.error('Error: End date must fall after start date.')  # Display an error message if the end date is before the start date
