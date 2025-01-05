import streamlit as st
import google.generativeai as genai
from styles import BACKGROUND_SVG, CSS
from config import GENERATION_CONFIG, SYSTEM_PROMPT
from utils import generate_unique_gradient, extract_topics_and_content

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

    # Fixed bottom input section
    with st.container():
        st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
        cols = st.columns([3, 1])
        with cols[0]:
            user_input = st.text_input("Enter a topic or number to explore:", 
                                    placeholder="e.g., Artificial Intelligence or '4'",
                                    key="fixed_input")
        with cols[1]:
            if st.button("Generate Topics", use_container_width=True):
                if user_input.strip():
                    try:
                        with st.spinner("Generating topics..."):
                            chat_session = st.session_state.gemini_model.start_chat(history=[])
                            response = chat_session.send_message(user_input)
                            topics_and_content = extract_topics_and_content(response.text)
                            
                            if topics_and_content:
                                st.session_state.topics_and_content = topics_and_content
                    except Exception as e:
                        st.error(f"Error during topic generation: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

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
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
