import streamlit as st


st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    
)

API_URL = "http://127.0.0.1:8000"


st.markdown(
    """
    <style>
        /* Set full-page background image */
        .stApp {
            background-image:  linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),url("https://admin.live.ilo.org/sites/default/files/styles/xx_wide/public/2024-07/ai-technology-brain-background-digital-transformation-concept.jpg?itok=QF0jKKdF");
            
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
            
        }
        .st-emotion-cache-h4xjwg{

        background : transparent; 
        
        }
        .main-title{
         animation: fadeInUp 0.7s ease-out forwards;
        text-align : center;
        }
        .subtitle{
         animation: fadeInUp 0.7s ease-out forwards;
        text-align : center;
        }
        
        .block-container{
        heigth : 100%
        width : 100%
        }
        .stMain{
        justify-content : center;
        }
        .stColumn{
        justify-content : center;
        }
        @keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}
        
        
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
# HTML structure for text and buttons
    st.markdown('<h1 class="main-title">Advanced AI-Powered Knowledge Retrieval</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Unlock the Full Potential of Your Data with AI</p>', unsafe_allow_html=True)
    
    st.html("template\index.html")
    #st.link_button("Start Exploring","http://localhost:8501/page_1")




