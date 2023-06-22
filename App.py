import streamlit as st  # Importing the Streamlit library for building interactive web apps
import streamlit.components.v1 as components  # Importing the components module from Streamlit
from streamlit_modal import Modal  # Importing the Modal component for creating modals
from Accueil import Accueil  # Importing the Accueil module
from Anomalie import Anomaile  # Importing the Anomalie module
from infraction_ import Infraction
from anomalie_ import Anomalie_
from RTD import rtd  # Importing the rtd module
from configuration import configuration  # Importing the configuration module
from streamlit_option_menu import option_menu  # Importing the option_menu component for creating dropdown menus
import os  # Importing the os module for file operations
import base64  # Importing the base64 module for encoding images

# Create a class to manage session state
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Function to retrieve the session state
def get_session() -> SessionState:
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = SessionState(username=None)
    return st.session_state['session_state']

# Get the session state
session_state = get_session()

# Main app function



def app(username: str):

    # Store the username passed to the app function
    user_name = username
    # Define the path to the user icon
    user_icon = "Assets/fd.png"

    # Use HTML to create the header with the user name and icon
    header_html = f"""
        <div id="header">
            <div id="user">
                <p id="user-name">{user_name}</p>
                <img id="user-image" src="data:image/png;base64,{base64.b64encode(open(user_icon, "rb").read()).decode()}">
            </div>
        </div>
    """

    # Display the header using Markdown
    st.markdown(header_html, unsafe_allow_html=True)

    # Apply custom CSS for the sidebar
    st.markdown('<style>' + open('./Style/sidebar.css').read() + '</style>', unsafe_allow_html=True)

    # Add sidebar components
    with st.sidebar:
        st.sidebar.image("Assets/LOGO.png")
        # Create a dropdown menu for selecting tabs
        tabs = option_menu(" ", ["Accueil", 'RTD Analytics', "Anomalie", "Infraction","Configuration"],
                           icons=['house', 'bar-chart-line',"person-bounding-box","signpost-split","gear-wide-connected"], default_index=0,
                           styles={
                               "container": {"background-color": "#FD673A", "border-radius": "0px"},
                               "icon": {"color": "#FFFFFF", "font-size": "20px"},
                               "nav-link": {"font-size": "19px", "text-align": "left", "margin": "0px",
                                            "--hover-color": "rgba(255, 255, 255, 0.20);", "color": "#FFFFFF;"},
                               "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.50);",
                                                     "font-size": "15px"},
                               "nav-item": {"color": "#FFFFFF;"},
                               "menu-title": {"color": "#FFFFFF;"}
                           })

    # Function to delete the session file
    def delete_session_file():
        if os.path.isfile('session_state.txt'):
            os.remove('session_state.txt')

    # Function to handle logout
    def logout():
        delete_session_file()
        session_state = get_session()
        session_state.username = None


    with st.sidebar:
        st.button("Déconnexion", on_click=logout,type="secondary",use_container_width=True,key=1)




    # Handle different tab selections and display corresponding content
    if tabs == "Accueil":
        Accueil()
    elif tabs == "RTD Analytics":
        rtd()
    elif tabs=="Anomalie":
        Anomalie_()
    elif tabs == "Infraction":
        Infraction()
    elif tabs == "Configuration":
        configuration()
