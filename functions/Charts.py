import streamlit as st  # Importing the Streamlit library for creating web apps
import plotly.express as px  # Importing the Plotly Express library for interactive plots
# import Database.database_caller  # Importing the database caller module
# import functions.data_checker  # Importing the data checker module
import pandas as pd
 # Caching data to improve performance

# Define a function named 'chart_par_classe' that takes five parameters: 'min_date1', 'max_date1', 'df', 'x', and 'label'
def chart_par_classe(df, x,label,max_date,min_date):

            if x == "Hour":
                label_date = "à l'heure:"
            else:
                label_date = "le jour"

            # Create a line plot using Plotly Express
            fig = px.line(df, x=x, y=['Total Classe 1', 'Total Classe 2', 'Total Classe 3'],
                          #color_discrete_map={'Total Classe 1': '#003f5c', 'Total Classe 2': '#ff6361', 'Total Classe 3': '#ffa600'},
                          title='Nombre de véhicules par classe',markers=True)
            
            fig.update_layout(width=1120, height=400)
            #fig.update_yaxes(tickmode='linear', dtick=1)
            fig.update_xaxes(tickmode='linear', dtick='D1')
   # Set the x-axis range
            fig.update_xaxes(range=[min_date - pd.Timedelta(days=1), max_date + pd.Timedelta(days=1)])
            fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
            # Exclude a small interval before the minimum date to create margin at the start of the line
            st.write(fig)




# Define a function named 'chart_par_sens' that takes five parameters: 'min_date1', 'max_date1', 'df', 'x', and 'label'
def chart_par_sens(df, x, label,max_date,min_date):
        if x == "Hour":
                label_date = "à l'heure:"
        else:
                label_date = "le jour"
            
            # Create a line plot using Plotly Express
        fig = px.line(df, x=x, y=['Sens 0', 'Sens 1'],
                          #color_discrete_map={'Total Classe 1': '#003f5c', 'Total Classe 2': '#ff6361', 'Total Classe 3': '#ffa600'},
                          title='Nombre de véhicules par Sens',markers=True)
            
        fig.update_layout(width=1120, height=400)
        #fig.update_yaxes(tickmode='linear', dtick=1)
        fig.update_xaxes(tickmode='linear', dtick='D1')
        #set the range x-axis
        fig.update_xaxes(range=[min_date - pd.Timedelta(days=1), max_date + pd.Timedelta(days=1)])
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.write(fig)