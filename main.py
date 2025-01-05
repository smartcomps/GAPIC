import streamlit as st
import google.generativeai as genai
from typing import Optional
import time
from config import GOOGLE_API_KEY, MAX_RETRIES, RATE_LIMIT_SECONDS
from styles import BACKGROUND_STYLE
from utils import generate_unique_gradient, sanitize_html, rate_limit

class LLMLibrary:
    def __init__(self):
        self.setup_page()
        self.initialize_gemini()
        
    def setup_page(self):
        """Setup page configuration and styling"""
        st.set_page_config(page_title="LLM Library", layout="wide")
        st.markdown(BACKGROUND_STYLE, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>LLM Library</h1>", unsafe_allow_html=True)
    
    def initialize_gemini(self):
        """Initialize Gemini API with error handling"""
        if not GOOGLE_API_KEY:
            st.error("Google API key not found. Please set it in your environment variables.")
            st.stop()
            
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8000,
                }
            )
        except Exception as e:
            st.error(f"Failed to initialize Gemini API: {str(e)}")
            st.stop()
    
    @staticmethod
    def extract_topics_and_content(ai_response: str) -> List[Dict[str, str]]:
        """Extract topics and content from AI response with error handling"""
        if not ai_response:
            return []
        
        topics_and_content = []
        try:
            sections = ai_response.split("**Topic")[1:]
            for section in sections:
                title = "Topic" + section.split("**")[0].strip()
                content = "**".join(section.split("**")[1:]).strip()
                # Sanitize content before storing
                content = sanitize_html(content)
                topics_and_content.append({"topic": title, "content": content})
        except Exception as e:
            st.error(f"Error parsing AI response: {str(e)}")
            return []
            
        return topics_and_content
    
    @rate_limit(RATE_LIMIT_SECONDS)
    def generate_topics(self, user_input: str) -> Optional[List[Dict[str, str]]]:
        """Generate topics with rate limiting and retry logic"""
        if not user_input.strip():
            st.warning("Please enter a topic or number.")
            return None
            
        for attempt in range(MAX_RETRIES):
            try:
                chat_session = self.model.start_chat(history=[])
                response = chat_session.send_message(user_input)
                return self.extract_topics_and_content(response.text)
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    st.error(f"Failed to generate topics after {MAX_RETRIES} attempts: {str(e)}")
                    return None
                time.sleep(1)  # Wait before retrying
    
    def render_topics_grid(self, topics_and_content: List[Dict[str, str]]):
        """Render topics in a responsive grid"""
        cols = st.columns(5)
        for idx, item in enumerate(topics_and_content):
            with cols[idx % 5]:
                gradient = generate_unique_gradient()
                st.markdown(
                    f"""
                    <div class="topic-box" style="background: {gradient};">
                        <h3>{item['topic']}</h3>
                        <p class="topic-preview">{item['content'][:80]}...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("View Full", key=f"view_full_{idx}"):
                    st.session_state.view_full = idx
                    st.experimental_rerun()
    
    def render_full_topic(self, topic_idx: int, topics_and_content: List[Dict[str, str]]):
        """Render full topic view"""
        topic = topics_and_content[topic_idx]
        if st.button("← Back to Topics"):
            del st.session_state.view_full
            st.experimental_rerun()
        
        st.markdown(f"### {topic['topic']}")
        st.markdown(topic['content'])
    
    def render_input_section(self):
        """Render the fixed bottom input section"""
        with st.container():
            st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
            cols = st.columns([3, 1])
            with cols[0]:
                user_input = st.text_input(
                    "Enter a topic or number to explore:",
                    placeholder="e.g., Artificial Intelligence or '4'",
                    key="fixed_input"
                )
            with cols[1]:
                if st.button("Generate Topics", use_container_width=True):
                    with st.spinner("Generating topics..."):
                        topics_and_content = self.generate_topics(user_input)
                        if topics_and_content:
                            st.session_state.topics_and_content = topics_and_content
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    app = LLMLibrary()
    app.render_input_section()
    
    if "topics_and_content" in st.session_state and st.session_state.topics_and_content:
        with st.container():
            st.markdown('<div class="content-padding">', unsafe_allow_html=True)
            
            if "view_full" in st.session_state:
                app.render_full_topic(
                    st.session_state.view_full,
                    st.session_state.topics_and_content
                )
            else:
                app.render_topics_grid(st.session_state.topics_and_content)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
