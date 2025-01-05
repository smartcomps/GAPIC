import streamlit as st
import random
import google.generativeai as genai
import re
import os

# Page config and UI setup
st.set_page_config(page_title="AI Topic Explorer", layout="wide")

# Add animated background and styles
st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;">
        <svg width="100" height="100" viewBox="0 0 100 100" style="position: absolute; top: 10%; left: 10%; animation: float1 20s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#1a73e8" style="opacity: 0.1;"/>
        </svg>
        <svg width="80" height="80" viewBox="0 0 100 100" style="position: absolute; top: 60%; left: 80%; animation: float2 25s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#4285f4" style="opacity: 0.1;"/>
        </svg>
        <svg width="120" height="120" viewBox="0 0 100 100" style="position: absolute; top: 80%; left: 20%; animation: float3 22s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#0f4fb8" style="opacity: 0.1;"/>
        </svg>
        <svg width="90" height="90" viewBox="0 0 100 100" style="position: absolute; top: 30%; left: 60%; animation: float4 28s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#1a73e8" style="opacity: 0.1;"/>
        </svg>
        <svg width="110" height="110" viewBox="0 0 100 100" style="position: absolute; top: 70%; left: 40%; animation: float5 24s infinite ease-in-out;">
            <polygon points="50,0 100,100 0,100" fill="#4285f4" style="opacity: 0.1;"/>
        </svg>
    </div>
""", unsafe_allow_html=True)

# Add styles including animations and modified topic box styling
st.markdown("""
    <style>
    @keyframes float1 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(100px, -100px) rotate(180deg); }
    }
    @keyframes float2 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-100px, 100px) rotate(-180deg); }
    }
    @keyframes float3 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(80px, -80px) rotate(120deg); }
    }
    @keyframes float4 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-80px, 80px) rotate(-120deg); }
    }
    @keyframes float5 {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(120px, -120px) rotate(240deg); }
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
    .topic-box h3 {
        font-size: 1em;
        margin-bottom: 10px;
    }
    .view-full-button {
        background-color: #1a73e8;
        color: white;
        padding: 6px 10px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        margin-top: 8px;
        width: 100%;
        font-size: 0.9em;
    }
    .view-full-button:hover {
        background-color: #0f4fb8;
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
""", unsafe_allow_html=True)

# Title centered at the top
st.markdown("<h1 style='text-align: center;'>AI Topic Explorer</h1>", unsafe_allow_html=True)

# Helper function for gradient generation
def generate_unique_gradient():
    color1 = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    color2 = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    return f"linear-gradient(135deg, {color1}, {color2})"

# Extract topics and contents from AI response
def extract_topics_and_content(ai_response):
    if not ai_response:
        return []
    
    topics_and_content = []
    sections = ai_response.split("**Topic")[1:]
    
    for section in sections:
        try:
            title = "Topic" + section.split("**")[0].strip()
            content = "**".join(section.split("**")[1:]).strip()
            topics_and_content.append({"topic": title, "content": content})
        except IndexError:
            continue
            
    return topics_and_content

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
                        # Configure Gemini only when needed
                        genai.configure(api_key="AIzaSyAFkjthP6CgmBu7CTTQmUf59v0HaJ7bjQ0")
                        
                        # Set up the model with system instruction
                        generation_config = {
                            "temperature": 1,
                            "top_p": 0.95,
                            "top_k": 40,
                            "max_output_tokens": 8000,
                            "response_mime_type": "text/plain",
                        }

                        model = genai.GenerativeModel(
                            model_name="gemini-2.0-flash-exp",
                            generation_config=generation_config,
                            system_instruction="""You are an AI designed to generate detailed, journalistic-style content on a wide array of topics. When provided with a broad topic or theme, you will randomly select a related subtopic or aspect to explore and craft a long-form, highly informative, and engaging article about it. Your role is to:

1. Understand the broad topic provided by the user.

2. Randomly select a related subtopic from within the scope of the main topic (e.g., if the user says "The Universe," you might explore black holes, stars, galaxies, or theories about the cosmos).

3. Generate a detailed, structured, and educational piece in a journalistic or storytelling tone. The content must:

Provide background and context on the subtopic.
Include key scientific, historical, or cultural details.
Engage the reader with examples, anecdotes, or relevant theories.
Conclude with insights, takeaways, or open questions to spark curiosity.

Be creative, but ensure factual accuracy, logical flow, and clarity. Your content should feel as though it was written by a knowledgeable journalist or storyteller deeply invested in the topic.

If no broad topic is provided and you receive a number from the user, you will independently choose the number of random subject specify by the number from a diverse range of fields (e.g., space, science, art, history, technology, culture) and generate content for each accordingly.Each topic should contain a huge amount of information in the style specify above

Format each topic as:
        **Topic 1: [Topic Name]**"""
                        )
                        
                        # Create chat session and send message
                        chat_session = model.start_chat(history=[])
                        response = chat_session.send_message(user_input)
                        
                        # Process response
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
