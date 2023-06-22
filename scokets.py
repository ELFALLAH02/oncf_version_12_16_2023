
import streamlit as st
import websockets
def send_message():
    ws = websockets.WebSocket()
    ws.connect('ws://localhost:8501')

    # Send a message to the C++ server
    message = 'ReloadTable'
    ws.send(message)

    # Close the WebSocket connection
    ws.close()

def main():
    st.write('Streamlit Web Page')

    # Create a button in the Streamlit app
    if st.button('Send Message'):
        send_message()
        st.write('Message sent to the C++ server')

if __name__ == '__main__':
    main()
