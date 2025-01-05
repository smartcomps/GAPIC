# main.py
import streamlit as st
import google.generativeai as genai
from styles import BACKGROUND_SVG, CSS
from config import GENERATION_CONFIG, SYSTEM_PROMPT
from utils import generate_unique_gradient, extract_topics_and_content

def process_input(input_text):
    """Process the input and generate topics"""
    try:
        with st.spinner("Generating topics..."):
            chat_session = st.session_state.gemini_model.start_chat(history=[])
            response = chat_session.send_message(input_text)
            topics_and_content = extract_topics_and_content(response.text)
            
            if topics_and_content:
                st.session_state.topics_and_content = topics_and_content
    except Exception as e:
        st.error(f"Error during topic generation: {e}")

def render_input_section(centered=False):
    """Render the input section either at bottom or centered"""
    style_class = "center-bottom" if centered else "fixed-bottom"
    
    container_style = f"""
    <style>
    .center-bottom {{
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 800px;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        border-radius: 10px 10px 0 0;
        margin-bottom: 0;
    }}
    .button-group {{
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-top: 10px;
    }}
    </style>
    """
    
    st.markdown(container_style, unsafe_allow_html=True)
    st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
    
    cols = st.columns([3, 1])
    with cols[0]:
        user_input = st.text_input("Enter a topic or number to explore:", 
                                placeholder="e.g., Artificial Intelligence or '4'",
                                key="fixed_input")
    with cols[1]:
        if st.button("Generate Topics", use_container_width=True):
            if user_input.strip():
                process_input(user_input)
    
    # Example button in its own container
    st.markdown('<div class="button-group">', unsafe_allow_html=True)
    if st.button("Ex", key="example_button"):
        process_input("5")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Page config and UI setup
    st.set_page_config(page_title="LLM Library", layout="wide")

    # Initialize Gemini only once at startup
    if 'gemini_model' not in st.session_state:
        genai.configure(api_key="AIzaSyAFkjthP6CgmBu7CTTQmUf59v0HaJ7bjQ0")
        st.session_state.gemini_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=GENERATION_CONFIG,
            system_instruction=SYSTEM_PROMPT
        )

    # Add animated background and styles
    st.markdown(BACKGROUND_SVG, unsafe_allow_html=True)
    st.markdown(CSS, unsafe_allow_html=True)

    # Title centered at the top
    st.markdown("<h1 style='text-align: center;'>LLM Library</h1>", unsafe_allow_html=True)

    # Display content area
    if "topics_and_content" in st.session_state and st.session_state.topics_and_content:
        with st.container():
            st.markdown('<div class="content-padding">', unsafe_allow_html=True)
            
            # Handle the "View Full" functionality
            if "view_full" in st.session_state:
                topic_idx = st.session_state.view_full
                topic = st.session_state.topics_and_content[topic_idx]
                
                if st.button("← Back to Topics"):
                    del st.session_state.view_full
                    st.experimental_rerun()
                
                st.markdown(f"### {topic['topic']}")
                st.markdown(topic['content'])
                # Render centered input when viewing a topic
                render_input_section(centered=True)
            else:
                # Display the generated topics in a 5-column grid
                cols = st.columns(5)
                for idx, item in enumerate(st.session_state.topics_and_content):
                    with cols[idx % 5]:
                        gradient = generate_unique_gradient()
                        st.markdown(f"""
                            <div class="topic-box" style="background: {gradient};">
                                <h3>{item['topic']}</h3>
                                <p class="topic-preview">
                                    {item['content'][:80]}...
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("View Full", key=f"view_full_{idx}"):
                            st.session_state.view_full = idx
                            st.experimental_rerun()
                
                # Render normal bottom input when viewing grid
                render_input_section(centered=False)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Render normal bottom input when no content
        render_input_section(centered=False)

if __name__ == "__main__":
    main()
