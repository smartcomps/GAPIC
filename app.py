import streamlit as st
import os
import google.generativeai as genai

# --- Configuration ---
API_KEY = "AIzaSyAxFKOLZzdteidIMOaNOHD6Y-alQfZgf08"  # Replace with your actual API key
MODEL_NAME = "gemini-1.5-flash"

# --- Model Setup ---
os.environ["GEMINI_API_KEY"] = API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    system_instruction=(
        "Your role is to design a specific user guide tailored for a particular user base. Begin by providing a brief introduction to the request, outlining the purpose and context of the guide. Ensure the guide is well-structured, with each instruction clearly stated and organized logically. Treat it like a mini-book that comprehensively describes what needs to be done and how to do it for the specified request. If the request involves code, you clearly explain each part of the code separately and conclude the guide with a fully structured example of the final code"
    ),
)

# --- Chat Function ---
def get_response(prompt):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            },
        ]
    )
    response = chat_session.send_message(prompt)
    return response.text

# --- Streamlit UI ---
st.markdown("<h1 style='text-align: center; color: white;'>Teaching Guide Bot</h1>", unsafe_allow_html=True)

with st.expander("Warning", expanded=False):
    st.write("Use With Caution")

st.write("Shows a level of explanation: ")
state = st.checkbox("Beginner")

if state:
    res = ""
    if text := st.chat_input("Write something: "):
        res = get_response(text)
        st.chat_message("user").markdown(text)
        with st.expander("ChatBot Compress message", expanded=False):
            st.write(res)
