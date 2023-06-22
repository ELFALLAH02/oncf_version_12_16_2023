import pandas as pd  # Import the pandas library for data manipulation and analysis
import streamlit as st  # Import the Streamlit library for building interactive web applications
import Database.Dataset  # Import the module for database communication
from App import app  # Import the app module that contains the main application logic
import hashlib  # Import the hashlib module for password hashing
import base64  # Import the base64 module for encoding and decoding data
import os  # Import the os module for interacting with the operating system

# Set the Streamlit page configuration
st.set_page_config(layout="wide", page_icon="Assets\FavIcon.png", page_title="IntelliTrain")

# Define a class for managing session state
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Function to retrieve the session state
def get_session():
    # Create a session state if it doesn't exist in st.session_state
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = SessionState(username=None)

    # Retrieve the session information from file
    if st.session_state['session_state'].username is None:
        session_state = st.session_state['session_state']
        if os.path.isfile('session_state.txt'):  # Check if the session state file exists
            with open('session_state.txt', 'r') as file:  # Open the file in read mode
                session_state.username = file.read()  # Read the username from the file

    return st.session_state['session_state']

# Function to save the session state
def save_session(session_state):
    # Save the session information to file
    with open('session_state.txt', 'w') as file:  # Open the file in write mode
        file.write(session_state.username)  # Write the username to the file

# Function for user login
def login():
    select_users=True

    if select_users:
        mydb, cursor =Database.Dataset.connect_to_database()
        def check_database_state(mydb):
            if not mydb.is_connected():
                mydb.connect()
        def get_column_names(cursor):
            return [desc[0] for desc in cursor.description]
        def user(username,password):
            check_database_state(mydb)
            cursor=mydb.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            return result
    
    # Apply custom CSS style for login form
    st.markdown('<style>' + open('./Style/login.css').read() + '</style>', unsafe_allow_html=True)

    # Function to hash the password
    def make_hashes(password):
        return hashlib.md5(password.encode()).hexdigest()

    # Function to check the hashed password
    def check_hashes(password, hashed_text):
        if make_hashes(password) == hashed_text:
            return hashed_text
        return False

    # Display the login form
    col_1, col_2, col_3 = st.columns([5, 4, 5])  # Create three columns for layout
    with col_2:
        col_icon_, col_icon, left = st.columns([2, 5, 2])  # Create three columns within the second column
        with col_icon:
            st.image(image="Assets/logo__.jpg")  # Display an image
        username = st.text_input("Nom d'utilisateur")  # Display a text input field for username
        password = st.text_input("Mot de passe ", type="password")  # Display a password input field
        login_button = st.button("Connexion")  # Display a button for login

        if login_button:  # Check if the login button is clicked
            # Check if the login credentials are valid
            hashed_pswd = make_hashes(password)  # Hash the password
            result =user(username, check_hashes(password, hashed_pswd))  # Call the user function from the database module
            if result:  # If the login is successful
                session_state.username = username  # Set the session state with the username
                save_session(session_state)  # Save the session state to a file
                st.experimental_rerun()  # Reload the app with the updated session state
            else:
                st.error("Invalid Nom d'utilisateur or Mot de passe!")  # Display an error message for invalid credentials

# Retrieve the session state
session_state = get_session()

# Check if the user is logged in
if session_state.username:  # If a username is present in the session state
    app(session_state.username)  # Call the desired page or function
else:
    login()  # Display the login form
