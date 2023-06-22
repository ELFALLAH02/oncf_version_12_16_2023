import streamlit as st
import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
import json
import math
from streamlit_drawable_canvas import st_canvas
import pandas as pd
from PIL import Image
import cv2
import streamlit_webrtc as webrtc
from streamlit_webrtc import webrtc_streamer,WebRtcMode
from glob import glob
from streamlit_image_annotation import detection
import av
import numpy as np
import streamlit.components.v1 as components
import Database.database_caller


def configuration():
    def df_to_dict(df):
        # Define the mapping of type values to integers
        type_mapping = {'Zone_comptage': 0, "Zone_intrusion": 1, "Zone_passage": 2}

        # Map the 'type' column values using the type_mapping dictionary
        df['type'] = df['type'].replace(type_mapping)

        # Create a dictionary to store the data
        data_dict = {
            'bboxes': df[['P1_X', 'P1_Y', 'P2_X', 'P2_Y']].values.tolist(),  # Convert the bounding box columns to a nested list
            'labels': df['type'].tolist(),  # Convert the 'type' column to a list
            "ID_zone": df["ID_zone"].tolist()  # Convert the 'ID_zone' column to a list
        }

        return data_dict
    zone = Database.database_caller.zones()
    # Slice the first 4 rows from the 'zones_data' DataFrame


    def read_index_html(copy_text: int):
        with open("Style/Config.html") as f:
            # Replace "python_string" in index.html with the value of copy_text
            return f.read().replace("python_string", f'"Counter value is {copy_text}"')

    # Load and apply custom CSS style from Config.css file
    st.markdown('<style>' + open('./Style/Config.css').read() + '</style>', unsafe_allow_html=True)

    # Split the screen into two columns
    col_camera_1, col_camera_2 = st.columns(2)

    # Set the value of rstp_rul variable
    rstp_rul = "rtsp://admin:mascir123@6.tcp.eu.ngrok.io:10736/cam/realmonitor?channel=1&subtype=2"


    with col_camera_1.expander("Camera view 1",expanded=True):  
                iframe_code = """
                <div><iframe width="500" height="400" src="https://rtsp.me/embed/kBFTntAQ/" frameborder="0" 
                allowfullscreen></iframe></div>
                """
                #Display the iframe code
                st.markdown(iframe_code, unsafe_allow_html=True)
    with col_camera_2.expander("Camera view 2",expanded=True):  
                iframe_code = """
                <div><iframe width="500" height="400" src="https://rtsp.me/embed/kBFTntAQ/" frameborder="0" 
                allowfullscreen></iframe></div>
                """
                # Display the iframe code
                st.markdown(iframe_code, unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["General", "RTD", "Infractions", "Anomalies"])

    # Display content under 'General' tab
    with tab1:
        col_side_save, col_annoation = st.columns([2, 8])

        # Display content in the left column
        with col_side_save:
            col_btn_json, col_btn_save = st.columns([2, 2])

            # Create buttons for saving and updating
            button1 = col_btn_json.button("Save")
            button2 = col_btn_save.button("Update")

        # Display content in the right column
        with col_annoation:
            # Retrieve a list of image paths from the 'images' directory
            image_path_list = glob('images/*.png')

            # Define a list of labels
            label_list = ["Zone_comptage", "Zone_intrusion", "Zone_passage"]

            # Initialize a dictionary to store annotation results
            result_dict = {}

            # Iterate over each image path
            for img in image_path_list:
                # Convert DataFrame 'zone' to a dictionary of annotations using 'df_to_dict' function
                annotations_dict = df_to_dict(zone)

                # Store the annotations dictionary in the result_dict using the image path as the key
                result_dict[img] = annotations_dict

                # Store the result_dict in the Streamlit session state
                st.session_state['result_dict'] = result_dict.copy()

            # Create a dropdown to select an image
            target_image_path = st.selectbox('Select an image:', image_path_list, index=0)

            # Call the 'detection' function with the selected image and annotations from session state
            new_labels = detection(
                image_path=target_image_path,
                label_list=label_list,
                bboxes=st.session_state['result_dict'][target_image_path]['bboxes'],
                labels=st.session_state['result_dict'][target_image_path]['labels'],
                key=target_image_path,
                width=700,
                height=800
            )
            if new_labels is not None:
                # Update the bounding boxes and labels in the session state with the newly obtained values
                st.session_state['result_dict'][target_image_path]['bboxes'] = [v['bbox'] for v in new_labels]
                st.session_state['result_dict'][target_image_path]['labels'] = [v['label_id'] for v in new_labels]
                

            # Check if the 'Save' button is clicked
            if button1:
                #Database.database_caller.update_zones(df)
                max_id_zone = Database.database_caller.max_zone()


                data = st.session_state['result_dict']
                rows = []

                for image_file, values in data.items():
                    bboxes = values["bboxes"]
                    labels = values["labels"]
                    id_zones = values["ID_zone"]
         
                    last_id_zone = None
                    id_zone_index = 0

                    for bbox, label in zip(bboxes, labels):
                        if id_zone_index < len(id_zones):
                            id_zone = id_zones[id_zone_index]
                            id_zone_index += 1
                        else:
                            if np.isnan(max_id_zone):
                                id_zone = np.nan
                            else:
                                id_zone = max_id_zone + 1
                                max_id_zone += 1
                            
                        max_id_zone= id_zone
                    
                        row = {
                            "ID_zone": id_zone,
                            "P1_X": bbox[0],
                            "P1_Y": bbox[1],
                            "P2_X": bbox[2],
                            "P2_Y": bbox[3],
                            "type": label
                        }
                        rows.append(row)

                dft = pd.DataFrame(rows)
                st.write(dft)
                type_mapping = { 0:'Zone_comptage',1:"Zone_intrusion",2:"Zone_passage"}

                # Map the 'type' column values using the type_mapping dictionary
                dft['type'] = dft['type'].replace(type_mapping)
                st.write(dft)
                #Database.database_caller.update_zones(dft)
                #Database.database_caller.insert_zone(dft)


#

            # Check if the 'Update' button is clicked
            if button2:
                # Display the result_dict as JSON
                st.json(result_dict)

                # Open the 'data.json' file for writing
                with open('data.json', 'w') as f:
                    # Save the result_dict as JSON in the file
                    json.dump(result_dict, f)

                # Display a message indicating that annotations are saved
                st.write('Annotations saved to annotations.json')


    with tab2:
        pass


    with tab3:
        pass
    with tab4:
        pass
    components.html(
            read_index_html(st.empty), # Read the HTML file and pass it to the 'html' parameter of the components.html() function
            height=0,
            width=0,
        )


