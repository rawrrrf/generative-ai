import streamlit as st
from PIL import Image
import groundingHelper


gh = groundingHelper.groundingHelper()

# CSS
imglogo = Image.open('RA_Logo_Bug-LeftText_white.jpg')
title_logo = Image.open('pagelogo.png')
# CSS

# CSS App title
st.set_page_config(
    page_title="Rok Chat",
    page_icon=title_logo,
    layout="wide"
)
# CSS

# Custom CSS changing side bar and footer
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #1B1C1E;
        z-index: 999;
        margin-top: 0;
    }
    [data-testid="stHeader"] {
        z-index:998;
    }   
    [data-testid="stSidebar"] img {
        width: 80%;
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 60px; /* Add margin bottom to increase spacing */        
    }
    [data-testid="stImage"] button {
        display: none; /* Hide the fullscreen button */
    }
    button[title="View fullscreen"]{
        opacity: 0 !important;
        transform: scale(1) !important;
    }        
    .off-white-text {
        color: #FFFFFF !important;
        font-size: 36px !important;
        margin-bottom: 20px;
    }
    .label {
        color: #FFFFFF !important;
        font-size: 22px;
    }
    .stAlert {
        background-color: coral !important;
        color: black !important;       
    }
    .stTextInput label {
        color: #F8F8FF; /* Off-white color */
    }
    .stAlert p {
        color: black; /* Black color */
    }
    [data-testid="stBottomBlockContainer"] {
        margin-bottom: 5px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-family: Arial, sans-serif;
        z-index: 1000;
    }
    .footer .dimmed-text {
        color: #BBBBBB; /* Dimmer white color */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# CSS

# CSS
# with st.sidebar:
#     st.image(imglogo)
    
    
#     st.markdown('<h1 class="off-white-text">ROKbot</h1>', unsafe_allow_html=True)
#     hf_email = st.text_input('Company Email:', type='password', key='email')
#     hf_pass = st.text_input('Password:', type='password', key='password')
    
#     if not (hf_email and hf_pass):
#         st.warning('  Please enter your credentials!', icon='⚠️')
#     else:
#         st.success('Great system starts here!')
# CSS

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Rokbot. How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# CSS Add the footer at the end
st.markdown(
    """
    <div class="footer">
        Rockwell Automation © 2024   <span class="dimmed-text">   Expanding human possibility.</span>
    </div>
    """,
    unsafe_allow_html=True
)
# CSS


# def generate_response_vertex(prompt_input):
    

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
response = ""
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = gh.chat.send_message(prompt, tools=[gh.tool])
            response = gh.print_grounding_response(ai_response)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)