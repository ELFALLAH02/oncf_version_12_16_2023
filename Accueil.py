
import streamlit as st
import Database.database_caller
from datetime import datetime

def Accueil():
    
    def Cards(Number,colors):
        Card = f""" 
          <div class="container">
              <div class="child-container">
                  <div class="rectangle">
                  </div>
                  <div class="side-rect" style="background:{colors}">
                      <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg"
                          style="flex-grow: 0; flex-shrink: 0;" preserveAspectRatio="none">
                          <path
                              d="M14.895 0.10498C6.70275 0.10498 0 6.80773 0 15C0 23.1922 6.70275 29.895 14.895 29.895C23.0873 29.895 29.79 23.1922 29.79 15C29.79 6.80773 23.0873 0.10498 14.895 0.10498ZM14.895 3.82873C21.0764 3.82873 26.0663 8.81856 26.0663 15C26.0663 21.1814 21.0764 26.1712 14.895 26.1712C8.71358 26.1712 3.72375 21.1814 3.72375 15C3.72375 8.81856 8.71358 3.82873 14.895 3.82873ZM14.895 7.55248C10.7989 7.55248 7.4475 10.9039 7.4475 15C7.4475 19.0961 10.7989 22.4475 14.895 22.4475C18.9911 22.4475 22.3425 19.0961 22.3425 15C22.3425 10.9039 18.9911 7.55248 14.895 7.55248ZM14.895 11.2762C16.9803 11.2762 18.6188 12.9147 18.6188 15C18.6188 17.0853 16.9803 18.7237 14.895 18.7237C12.8097 18.7237 11.1713 17.0853 11.1713 15C11.1713 12.9147 12.8097 11.2762 14.895 11.2762Z"
                              fill="white"></path>
                      </svg>
                  </div>
                  <div class="Content-container">
                      <p class="label">
                          Nombre total infraction
                      </p>
                      <p class="Number">
                          {Number}
                      </p>
                  </div>
              </div>
          </div>"""
        return Card
    st.markdown('<style>' + open('./Style/Card.css').read() + '</style>', unsafe_allow_html=True)

    col_header_1,col_header_2,col_header_3,col_header_4=st.columns([2,2,2,2],gap="medium")
    with col_header_1:
           Number=121
           colors="#4569e8;"
           st.markdown(Cards(Number,colors), unsafe_allow_html=True)
    with col_header_2:
           colors="#45A3E8;"
           Number=325
           st.markdown(Cards(Number,colors), unsafe_allow_html=True)

    with col_header_3:
           colors="#023540;"

           Number=232
           st.markdown(Cards(Number,colors), unsafe_allow_html=True)
    with col_header_4:
           colors="#E86F45;"
           Number=235
           st.markdown(Cards(Number,colors), unsafe_allow_html=True)

    col_camera,col_man=st.columns([5,2])
    def camera_1(IP_camera_1,state):
            camera_1=f"""
                <div class="container-IP-camera">
                                <p class="text-IP-camera">{IP_camera_1 +":"}</p>
                                    <svg class="circle_" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"
                                                    preserveAspectRatio="none">
                                        <circle cx="9" cy="9" r="9" fill="{state}"></circle>
                                    </svg>
                </div>"""
            return camera_1
    def camera_2(IP_camera_2,state):
            camera_2=f"""
                <div class="container-IP-camera">
                                <p class="text-IP-camera">{IP_camera_2 +":"}</p>
                                <svg class="circle_" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"
                                    preserveAspectRatio="none">
                                    <circle cx="9" cy="9" r="9" fill="{state}"></circle>
                                </svg>
                </div>"""
            return camera_2
    def camera_state(state):
            camera_status=f"""
                <div class="container-IP-camera">
                                <p class="text-IP-camera">Status de fonctionnement :</p>
                                <svg  class="circle_" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"
                                     preserveAspectRatio="none">
                                    <circle cx="9" cy="9" r="9" fill="{state}"></circle>
                                </svg>
                </div>"""
            return camera_status
    with col_camera :
        col1,col_empty=st.columns(2)
        with col1:
            st.write("Info system")
        with col_empty:
            pass
        #-----------#
        col_camera1,col_camera2,col_status=st.columns(3)
        with col_camera1:
                IP_camera_1="12FD2666F6ERRERF"
                state="#128A11"
                st.markdown(camera_1(IP_camera_1,state), unsafe_allow_html=True)
        with col_camera2:
                IP_camera_2="12FD2666F6ERRERF"
                state="#128A11"
                st.markdown(camera_2(IP_camera_2,state), unsafe_allow_html=True)
        with col_status:
                state="#128A11"
                st.markdown(camera_state(state), unsafe_allow_html=True)                                

      #st.markdown(Info_System(IP_camera_1,IP_camera_2,state), unsafe_allow_html=True)
    with col_man:
        col2,col_empty_=st.columns(2)
        with col2:
            st.write("Mode maintenance")
        with col_empty_:
            pass

        st.radio(" ",["Activate","Desactivé"],horizontal=True)
    col_left_3,col_bar,col_right_3=st.columns([0.01,10,0.01])
    with col_bar:
        col_section_1,col_section_2,col_section_3=st.columns([4,1,1])
        if 'min_date3' not in st.session_state:
                st.session_state.min_date3 = datetime.now()
                st.session_state.max_date3 =  datetime.now()
            # Retrieve the current values of min_date3 and max_date3 from session state
        min_date3 = st.session_state.min_date3
        max_date3 = st.session_state.max_date3

            # Create a date range selector and update min_date3 and max_date3 accordingly
        v = col_section_3.date_input(" ", (min_date3, max_date3), max_value=datetime.now())
        if len(v) == 2:
                st.session_state.min_date3 = v[0]
                st.session_state.max_date3 = v[1]
        else:
                print("error")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    cpl_section_container_3_0,cpl_section_container_3_1,cpl_section_container_3_2=st.columns([0.01,10,0.01])
    with cpl_section_container_3_1:
        col_title,col_time_select,col=st.columns([4,1,1])
        with col_title:
           st.write("Infraction")
        with col_time_select:
            if 'min_date2' not in st.session_state:
                st.session_state.min_date2 =  datetime.now()
                st.session_state.max_date2 =  datetime.now()

                # Retrieve the current values of min_date3 and max_date3 from session state
            min_date2 = st.session_state.min_date2
            max_date2 = st.session_state.max_date2

                # Create a date range selector and update min_date3 and max_date3 accordingly
            v = col.date_input("  ", (min_date2, max_date2), max_value= datetime.now())
            if len(v) == 2:
                    st.session_state.min_date2 = v[0]
                    st.session_state.max_date2= v[1]
            else:
                    print("error")
        col_,col_section_3_1,col_section_3_2,col_section_3_3=st.columns([0.9,2,2,2])
        with col_section_3_1:
            st.write("Acte de malveillance :")
        with col_section_3_2:
            st.write("Intrusion :")
        with col_section_3_3:
            st.write("Masquage caméra : ")