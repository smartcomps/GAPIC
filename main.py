import streamlit as st
import random
import google.generativeai as genai
import re
import os
import time
from functools import wraps
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MAX_RETRIES = 3
RATE_LIMIT_SECONDS = 1

# Styles
BACKGROUND_STYLE = """
    <style>
    @keyframes float1 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(100px, -100px) rotate(180deg); }
    }
    
    .stApp {
        background-color: white;
        color: #333333;
    }
    .topic-box {
        border-radius: 12px;
        margin-bottom: 20px;
        padding: 15px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        color: white;
        height: 200px;
        display: flex;
        flex-direction: column;
    }
    .topic-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
    }
    .topic-preview {
        color: white;
        padding: 8px;
        border-radius: 8px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        white-space: normal;
        background: rgba(255, 255, 255, 0.2);
        flex-grow: 1;
        font-size: 0.9em;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .content-padding {
        padding-bottom: 100px;
        position: relative;
        z-index: 1;
    }
    </style>
"""

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
    
    def rate_limit(seconds: int):
        """Rate limiting decorator"""
        last_run = {}
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                if func.__name__ in last_run and now - last_run[func.__name__] < seconds:
                    raise Exception("Please wait before making another request")
                last_run[func.__name__] = now
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def generate_unique_gradient(self) -> str:
        """Generate a unique gradient with safe color combinations"""
        def generate_safe_color():
            return f"#{random.randint(30, 200):02x}{random.randint(30, 200):02x}{random.randint(30, 200):02x}"
        
        return f"linear-gradient(135deg, {generate_safe_color()}, {generate_safe_color()})"

    @staticmethod
    def sanitize_html(text: str) -> str:
        """Sanitize HTML content"""
        dangerous_tags = ['script', 'style', 'iframe', 'object', 'embed']
        for tag in dangerous_tags:
            text = re.sub(f'<{tag}.*?</{tag}>', '', text, flags=re.DOTALL)
        return text
    
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
                content = LLMLibrary.sanitize_html(content)
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
                time.sleep(1)
    
    def render_topics_grid(self, topics_and_content: List[Dict[str, str]]):
        """Render topics in a responsive grid"""
        cols = st.columns(5)
        for idx, item in enumerate(topics_and_content):
            with cols[idx % 5]:
                gradient = self.generate_unique_gradient()
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
