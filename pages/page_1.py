import streamlit as st
import requests


st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",

)

API_URL = "http://127.0.0.1:8000"

st.subheader("Choose Query Type : ")

option = st.selectbox("", ("Upload File", "YouTube Video", "Query"))

if option == "Query":
     question =st.chat_input("Generate AI Response")
    
     if question:
        # A placeholder to update with streaming text
        with st.chat_message("assistant"):
            placeholder = st.empty()
            accumulated_text = ""
        
        # Call the API endpoint with streaming enabled
        params = {"question": question}
        
        with requests.get(f"{API_URL}/query", params=params, stream=True) as response:
            # Iterate over lines (chunks) in the streaming response
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8").strip()

                # Add spacing & new lines properly
                    accumulated_text += decoded_line + "\n"

                # Display dynamically using markdown
                    placeholder.markdown(accumulated_text, unsafe_allow_html=True)

elif option == "Upload File":
    st.subheader("Upload a File")
    uploaded_file = st.file_uploader("", type=["pdf", "txt"])
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{API_URL}/upload", files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            st.json(response.json())
        else:
            st.error(f"Error uploading file: {response.text}")

elif option == "YouTube Video":
    st.subheader("Process YouTube Video")
    video_url = st.text_input("Enter YouTube Video URL")
    if st.button("Process Video") and video_url:
        params = {"video_url": video_url}
        response = requests.post(f"{API_URL}/youtube", params=params)
        if response.status_code == 200:
            st.success("YouTube link processed successfully!")
            st.json(response.json())
        else:
            st.error(f"Error processing YouTube link: {response.text}")

